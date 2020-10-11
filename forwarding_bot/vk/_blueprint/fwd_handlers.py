import logging
from collections import namedtuple
from typing import Dict
from typing import List

from aiohttp import ClientSession
from vkbottle.types.objects.messages import Message
from vkbottle.types.objects.users import UserXtrCounters

from forwarding_bot.config import data_config
from .helpers import MessageHelper, RequestHelper
from .settings import api_url

logger = logging.getLogger("forwarding-bot")


async def handle_fwd(
        session: ClientSession,
        request_params: dict,
        message: Message
) -> None:
    """Handle nested forwarded messages"""
    # TODO: Add logging
    # TODO: Add photo, document, voice support
    # TODO: Add HTML multicolor for senders and bold red for docs and photos
    sender_cache: Dict[int, UserXtrCounters] = {}
    ParsedMessage = namedtuple("ParsedMessage", "sender text indent")
    result: List[ParsedMessage] = []

    async def walk_message_tree(node: Message, depth: int = 0):
        if message.from_id in sender_cache:
            sender = sender_cache[message.from_id]
        else:
            sender = await MessageHelper.get_sender(data_config.group_token, message)
            sender_cache[message.from_id] = sender

        result.append(ParsedMessage(
            MessageHelper.get_name(sender),
            MessageHelper.get_text(node.text),
            depth
        ))

        children = node.fwd_messages or []
        for child in children:
            await walk_message_tree(child, depth + 1)

    await walk_message_tree(message)

    message_text = ""
    for msg in result:
        message_text += "{indent}{sender}:\n{indent}{text}".format(
            # Replaced tab with 4 spaces to add indent consistency
            indent="    " * msg.indent,
            sender=msg.sender,
            # Avoid \n on empty text
            text=msg.text + "\n" if msg.text else ""
        )

    request_params["text"] = message_text
    response = await session.get(api_url + "sendMessage", params=request_params)
    await RequestHelper.response_check(response)
