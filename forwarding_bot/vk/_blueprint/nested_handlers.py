import logging
from typing import Dict, List
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


def parse_text(message_: ParsedMessage, attachment_storage: List) -> str:
    if not message_.text and not message_.attachments:
        return ""
    if message_.text:
        text = "    " * message_.indent + MessageHelper.get_text(message_.text) + "\n"
    else:
        text = ""

    attach_names = {"doc": "документ", "photo": "фото"}

    for attach_ in message_.attachments:
        attachment_storage.append(attach_)
        text += '{indent}<u>{{{name}_{id}}}</u>\n'.format(indent="    " * message_.indent,
                                                          name=attach_names[str(attach_.type)],
                                                          id=len(attachment_storage))
    return text


async def handle_nested(
        bot: Bot,
        message: Message
):
    """Handle nested forwarded messages"""
    attachments: List[MessageAttachment] = []
    tree = await get_tree(message)
    logger.debug("Got tree")

    message_text = ""
    for msg in tree:
        message_text += "{indent}{sender}:\n{text}".format(
            # Replaced tab with 4 spaces to add indent consistency
            indent="    " * msg.indent,
            sender=msg.sender,
            # Avoid \n on empty text
            text=parse_text(message_=msg, attachment_storage=attachments)
        )

    logger.debug("Parsed messages")

    await bot.send_message(chat_id=data_config.destination_id,
                           text=message_text,
                           parse_mode=data_config.parse_mode)

    logger.info("Sent text, sending docs...")

    for num, attach in enumerate(attachments, 1):
        if attach.type == "photo":
            source = max(attach.photo.sizes, key=lambda size: size.width)
            await bot.send_photo(chat_id=data_config.destination_id,
                                 caption=f"фото_{num}",
                                 photo=source.url,
                                 parse_mode=data_config.parse_mode)
            logger.debug("sent photo")
        elif attach.type == "doc":
            data = types.InputFile.from_url(url=attach.doc.url,
                                            filename=attach.doc.title)
            await bot.send_document(chat_id=data_config.destination_id,
                                    caption=f"документ_{num}",
                                    document=data,
                                    parse_mode=data_config.parse_mode)
            logger.debug("sent document")
