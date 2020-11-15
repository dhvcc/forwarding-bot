import logging
from asyncio import sleep

from aiogram import Bot
from vkbottle.user import Blueprint, Message
from typing import NoReturn
from forwarding_bot.config import data_config
from forwarding_bot.settings import PARSE_MODE
from . import attachment_handler, nested_handler
from .message_helper import MessageHelper

logger = logging.getLogger(__name__)

bot_bp = Blueprint()


@bot_bp.on.chat_message()
async def handler(message: Message) -> NoReturn:
    """Default handler that handles every message"""
    logger.info("New message")
    logger.debug(str(message))
    # VK attachment limit workaround
    # Also needed to have right model parsing
    logger.debug("Requesting message data")
    message_data = (await bot_bp.api.messages.get_by_id(message_ids=[message.id])).items[0]
    message.attachments = message_data.attachments
    message.fwd_messages = message_data.fwd_messages
    #
    logger.debug("Requesting sender and attachments")
    bot = Bot(data_config.bot_token)
    sender = await MessageHelper.get_sender(data_config.user_token, message)
    attachments = MessageHelper.get_valid_attachments(message)

    message_template = "{head}:\n{text}"
    formatted_message = message_template.format(head=MessageHelper.get_header(sender, message),
                                                text=MessageHelper.get_text(message.text))

    # This is horrible, I know
    if message.fwd_messages:
        await nested_handler.handle_nested(bot=bot, message=message, tree_getter=nested_handler.get_fwd_tree)
    elif message.reply_message:
        await nested_handler.handle_nested(bot=bot, message=message, tree_getter=nested_handler.get_reply_tree)
    elif len(attachments) == 1:
        logger.info("One attachment, calling handler")
        await attachment_handler.handle_attachment(
            bot,
            formatted_message,
            attachments[0]
        )
    elif message.attachments:
        await nested_handler.handle_nested(bot=bot, message=message, tree_getter=nested_handler.get_fwd_tree)
    elif not message.attachments:
        logger.info("No valid attachments or forwarded messages, sending text")
        await bot.send_message(chat_id=data_config.destination_id,
                               text=formatted_message,
                               parse_mode=PARSE_MODE)

    await bot.close()
    await sleep(0.1)
