import logging
from asyncio import sleep

import aiohttp
from vkbottle.bot import Blueprint, Message

from forwarding_bot.config import data_config
from . import attachment_handlers
from . import utils

logger = logging.getLogger("forwarding-bot")

bot_bp = Blueprint()


@bot_bp.on.chat_message()
async def handler(message: Message) -> None:
    """Default handler that catches any message"""

    sender = await utils.get_sender(data_config.group_token, message)
    request_params = utils.basic_params(bot=bot_bp)
    formatted_message = utils.format_message(sender, message)
    attachments = utils.get_valid_attachments(message)

    async with aiohttp.ClientSession() as session:
        try:
            if not attachments:
                await attachment_handlers.no_attachments(
                    session,
                    request_params,
                    formatted_message
                )
            elif len(attachments) == 1:
                await attachment_handlers.one_attachment(
                    session,
                    request_params,
                    formatted_message,
                    attachments[0]
                )
            else:
                await attachment_handlers.more_attachments(
                    session,
                    request_params,
                    formatted_message,
                    attachments
                )
        except utils.BadDoctypeError as e:
            await message(str(e))
    await sleep(0.1)
