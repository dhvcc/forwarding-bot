import logging
from collections import namedtuple
from typing import Dict, List

from aiohttp import ClientSession
from vkbottle.types.objects.messages import Message, MessageAttachment
from vkbottle.types.objects.users import UserXtrCounters

from forwarding_bot.config import data_config
from .helpers import MessageHelper, RequestHelper
from .settings import api_url

logger = logging.getLogger("forwarding-bot")

ATTACH_INFO = {
    "photo": {"name": "фото", "handler": RequestHelper.send_photo, "selector": lambda a: a.photo},
    "doc": {"name": "документ", "handler": RequestHelper.send_document, "selector": lambda a: a.doc}
}


async def handle_fwd(
        session: ClientSession,
        request_params: dict,
        message: Message
) -> None:
    """Handle nested forwarded messages"""
    # TODO: Add logging
    # TODO: Add photo, document, voice support
    sender_cache: Dict[int, UserXtrCounters] = {}
    ParsedMessage = namedtuple("ParsedMessage", "sender text attachments indent")
    attachments: List[MessageAttachment] = []
    result: List[ParsedMessage] = []

    async def walk_message_tree(node: Message, depth: int = 0):
        if message.from_id in sender_cache:
            sender = sender_cache[message.from_id]
        else:
            sender = await MessageHelper.get_sender(data_config.group_token, message)
            sender_cache[message.from_id] = sender

        result.append(ParsedMessage(
            MessageHelper.get_name(sender),
            node.text,
            MessageHelper.get_valid_attachments(node),
            depth
        ))

        children = node.fwd_messages or []
        for child in children:
            await walk_message_tree(child, depth + 1)

    await walk_message_tree(message)

    def parse_text(message_: ParsedMessage) -> str:
        if not message_.text and not message_.attachments:
            return ""
        if message_.text:
            text = "    " * message_.indent + MessageHelper.get_text(message_.text) + "\n"
        else:
            text = ""
        for attach_ in message_.attachments:
            attachments.append(attach_)
            text += '{indent}<u>{{{name}_{id}}}</u>\n'.format(indent="    " * msg.indent,
                                                              name=ATTACH_INFO[attach_.type]["name"],
                                                              id=len(attachments))
        return text

    message_text = ""
    for msg in result:
        message_text += "{indent}{sender}:\n{text}".format(
            # Replaced tab with 4 spaces to add indent consistency
            indent="    " * msg.indent,
            sender=msg.sender,
            # Avoid \n on empty text
            text=parse_text(msg)
        )

    request_params["text"] = message_text
    response = await session.get(api_url + "sendMessage", params=request_params)
    await RequestHelper.response_check(response)

    request_params.pop("text")

    for num, attach in enumerate(attachments, 1):
        try:
            info = ATTACH_INFO[str(attach.type)]
        except KeyError:
            continue
        request_params["caption"] = "{{{name}_{id}}}".format(name=info["name"],
                                                             id=num)
        response = await info["handler"](session, info["selector"](attach), request_params)
        await RequestHelper.response_check(response)
