import logging
from typing import Dict, List, Tuple, NamedTuple, NoReturn, Coroutine, Callable

from aiogram import Bot, types
from vkbottle.types.objects.messages import Message, MessageAttachment
from vkbottle.types.objects.users import UserXtrCounters

from forwarding_bot.config import data_config
from forwarding_bot.settings import PARSE_MODE
from .message_helper import MessageHelper

logger = logging.getLogger(__name__)

ParsedMessage = NamedTuple(
    "ParsedMessage",
    [
        ("sender", str),
        ("text", str),
        ("attachments", List[MessageAttachment]),
        ("indent", int)
    ]
)


async def get_fwd_tree(root: Message) -> List[ParsedMessage]:
    sender_cache: Dict[int, UserXtrCounters] = {}
    result: List[ParsedMessage] = []

    async def walk_message_tree(node: Message, depth: int = 0):
        if node.from_id in sender_cache:
            sender = sender_cache[node.from_id]
        else:
            sender = await MessageHelper.get_sender(data_config.user_token, node)
            sender_cache[node.from_id] = sender

        if node.text or node.attachments:
            result.append(ParsedMessage(
                sender=MessageHelper.get_header(sender, node),
                text=node.text,
                attachments=MessageHelper.get_valid_attachments(node),
                indent=depth,
            ))
            depth += 1

        children = node.fwd_messages or []

        for child in children:
            await walk_message_tree(child, depth)

    await walk_message_tree(root)

    return result


async def get_reply_tree(root: Message) -> List[ParsedMessage]:
    sender_cache: Dict[int, UserXtrCounters] = {}
    result: List[ParsedMessage] = []
    # Result will consist of only reply (without attachments, text limited to 100 chars)

    # Reply message
    reply = root

    if reply.from_id in sender_cache:
        sender = sender_cache[reply.from_id]
    else:
        sender = await MessageHelper.get_sender(data_config.user_token, reply)

    if reply.text or reply.attachments:
        result.append(ParsedMessage(
            sender=MessageHelper.get_header(sender, reply),
            text=reply.text,
            attachments=MessageHelper.get_valid_attachments(reply),
            indent=0,
        ))

    #  Reply target
    reply_target = root.reply_message

    text = reply_target.text[:97] or "*вложения без текста*"
    if len(reply_target.text) > 97:
        text += "..."

    sender = await MessageHelper.get_sender(data_config.user_token, reply_target)
    sender_cache[sender.id] = sender

    result.append(ParsedMessage(
        sender=MessageHelper.get_header(sender, reply_target),
        text=text,
        attachments=[],
        indent=1,
    ))

    return result


def parse_text(message_: ParsedMessage, attachment_storage: List[Tuple[str, MessageAttachment]]) -> str:
    if not message_.text and not message_.attachments:
        return ""
    if message_.text:
        # If text itself contains \n then they should be prefixed with indent
        split_text = MessageHelper.get_text(message_.text).split("\n")
        indent_str = "    " * message_.indent
        parsed_list = [f"{indent_str}{text}\n" for text in split_text]
        text = "".join(parsed_list)
    else:
        text = ""

    attach_names = {
        "audio_message": "голосовое_сообщение",
        "doc": "документ",
        "photo": "фото",
    }

    for attach_ in message_.attachments:
        name = "{name}_{id}".format(name=attach_names[str(attach_.type)],
                                    id=len(attachment_storage))
        attachment_storage.append((name, attach_))
        text += '{indent}<u>{{{name}}}</u>\n'.format(indent="    " * message_.indent,
                                                     name=name)

    return text


async def handle_nested(
        bot: Bot,
        message: Message,
        tree_getter: Callable[..., Coroutine]
) -> NoReturn:
    """
    Handle nested forwarded messages
    1. Parse message tree
    2. Parse output text, add {} to insert message references with .format()
    3. Send attachments and generate references
    4. Format text and insert references, send the text
    """
    attachments: List[Tuple[str, MessageAttachment]] = []
    message_references: Dict[str, str] = {}
    tree = await tree_getter(message)
    logger.debug("Got tree")

    # Prepare text, insert {} and append to attachments
    message_text = ""
    for msg in tree:
        message_text += "{indent}{sender}:\n{text}".format(
            # Replaced tab with 4 spaces to add indent consistency
            indent="    " * msg.indent,
            sender=msg.sender,
            # Avoid \n on empty text
            text=parse_text(message_=msg, attachment_storage=attachments)
        )
    logger.debug("Prepared text, sending attachments...")

    # Send attachments
    for name, attach in attachments:
        if attach.type == "photo":
            source = max(attach.photo.sizes, key=lambda size: size.width)
            response = await bot.send_photo(chat_id=data_config.destination_id,
                                            caption=name,
                                            photo=source.url,
                                            parse_mode=PARSE_MODE)
            logger.debug("sent photo")
        elif attach.type == "audio_message":
            response = await bot.send_voice(chat_id=data_config.destination_id,
                                            caption=name,
                                            voice=attach.audio_message.link_ogg,
                                            parse_mode=PARSE_MODE)
        else:
            data = types.InputFile.from_url(url=attach.doc.url,
                                            filename=attach.doc.title)
            response = await bot.send_document(chat_id=data_config.destination_id,
                                               caption=name,
                                               document=data,
                                               parse_mode=PARSE_MODE)
            logger.debug("sent document")

        # response.chat_id is -10...0chat_id, so [2:] cuts the '-1' out
        message_references[name] = f'<a href="https://t.me/c/{str(response.chat.id)[2:]}/{response.message_id}">' \
                                   f'{name}' \
                                   f'</a>'
    logger.debug("Sent attachments, sending text...")

    await bot.send_message(chat_id=data_config.destination_id,
                           text=message_text.format(**message_references),
                           parse_mode=PARSE_MODE)

    # May be collect the responses and return them as a list?
    logger.info("Sent text")
