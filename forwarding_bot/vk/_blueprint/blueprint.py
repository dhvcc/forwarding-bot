import logging
from asyncio import sleep

import aiohttp
from vkbottle.bot import Blueprint, Message

from forwarding_bot.config import data_config
from .utils import Utils, BadRequestError
from .attachment_handlers import AttachmentHandlers

logger = logging.getLogger()

bot_bp = Blueprint()


@bot_bp.on.chat_message()
async def handler(message: Message) -> None:
    """Default handler that catches any message"""

    sender = await Utils.get_sender(data_config.group_token, message)
    request_params = Utils.basic_params(bot=bot_bp)
    tg_message = Utils.format_message(sender, message)
    attachments = Utils.get_valid_attachments(message)

    async with aiohttp.ClientSession() as session:
        try:
            if not attachments:
                await AttachmentHandlers.no_attachments(session, request_params, tg_message)
            elif len(attachments) == 1:
                await AttachmentHandlers.one_attachment(session, request_params, attachments, tg_message)
            else:
                await AttachmentHandlers.more_attachments(session, request_params, attachments, tg_message)
        except BadRequestError as e:
            await message(str(e))
    await sleep(0.1)
