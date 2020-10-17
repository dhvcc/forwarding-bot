import logging
from asyncio import sleep

from aiogram import Bot
from vkbottle.user import Blueprint, Message

from forwarding_bot.config import data_config
from . import attachment_handlers, nested_handlers
from .message_helper import MessageHelper

logger = logging.getLogger("forwarding-bot")

bot_bp = Blueprint()


@bot_bp.on.chat_message()
async def handler(message: Message) -> None:
    """Default handler that handles every message"""
    # VK attachment limit workaround
    # Also needed to have right model parsing
    message_data = (await bot_bp.api.messages.get_by_id(message_ids=[message.id])).items[0]
    message.attachments = message_data.attachments
    message.fwd_messages = message_data.fwd_messages
    #

    bot = Bot(data_config.bot_token)
    sender = await MessageHelper.get_sender(data_config.user_token, message)
    attachments = MessageHelper.get_valid_attachments(message)

    message_template = "{head}:\n{text}"
    formatted_message = message_template.format(head=MessageHelper.get_header(sender, message),
                                                text=MessageHelper.get_text(message.text))

    if not attachments and not message.fwd_messages:
        await bot.send_message(chat_id=data_config.destination_id,
                               text=formatted_message,
                               parse_mode=data_config.parse_mode)
    elif len(attachments) == 1 and not message.fwd_messages:
        await attachment_handlers.one_attachment(
            bot,
            formatted_message,
            attachments[0]
        )
    else:
        await nested_handlers.handle_nested(bot=bot, message=message)

    await bot.close()
    await sleep(0.1)
