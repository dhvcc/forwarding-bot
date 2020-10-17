import logging
from typing import Dict, List, Tuple
from typing import NamedTuple

from aiogram import Bot, types
from vkbottle.types.objects.messages import Message, MessageAttachment
from vkbottle.types.objects.users import UserXtrCounters

from forwarding_bot.config import data_config
from .message_helper import MessageHelper

logger = logging.getLogger("forwarding-bot")

ParsedMessage = NamedTuple(
    "ParsedMessage",
    [
        ("sender", UserXtrCounters),
        ("text", str),
        ("attachments", List[MessageAttachment]),
        ("indent", int)
    ]
)


async def get_tree(root: Message):
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


def parse_text(message_: ParsedMessage, attachment_storage: List[Tuple[str, MessageAttachment]]) -> str:
    if not message_.text and not message_.attachments:
        return ""
    if message_.text:
        text = "    " * message_.indent + MessageHelper.get_text(message_.text) + "\n"
    else:
        text = ""

    attach_names = {"doc": "документ", "photo": "фото"}

    for attach_ in message_.attachments:
        name = "{name}_{id}".format(name=attach_names[str(attach_.type)],
                                    id=len(attachment_storage))
        attachment_storage.append((name, attach_))
        text += '{indent}<u>{{{name}}}</u>\n'.format(indent="    " * message_.indent,
                                                     name=name)
    return text


async def handle_nested(
        bot: Bot,
        message: Message
):
    """Handle nested forwarded messages"""
    attachments: List[Tuple[str, MessageAttachment]] = []
    message_references: Dict[str, str] = {}
    tree = await get_tree(message)
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
            resp = await bot.send_photo(chat_id=data_config.destination_id,
                                        caption=name,
                                        photo=source.url,
                                        parse_mode=data_config.parse_mode)
            logger.debug("sent photo")
        else:
            data = types.InputFile.from_url(url=attach.doc.url,
                                            filename=attach.doc.title)
            resp = await bot.send_document(chat_id=data_config.destination_id,
                                           caption=name,
                                           document=data,
                                           parse_mode=data_config.parse_mode)
            logger.debug("sent document")

        message_references[name] = f'<a href="https://t.me/c/{str(resp.chat.id)[2:]}/{resp.message_id}">{name}</a>'
    logger.debug("Sent attachments, sending text...")

    await bot.send_message(chat_id=data_config.destination_id,
                           text=message_text.format(**message_references),
                           parse_mode=data_config.parse_mode)

    logger.info("Sent text")
