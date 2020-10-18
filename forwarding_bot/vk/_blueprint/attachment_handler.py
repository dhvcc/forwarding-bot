import logging

from aiogram import Bot, types
from vkbottle.types.objects.messages import MessageAttachment

from forwarding_bot.config import data_config
from forwarding_bot.settings import PARSE_MODE

logger = logging.getLogger(__name__)


async def handle_attachment(
        bot: Bot,
        message_text: str,
        msg_attachment: MessageAttachment,
) -> types.Message:
    logger.debug(f"One attachment with type {msg_attachment.type}")
    if msg_attachment.type == "sticker":
        response = await bot.send_message(chat_id=data_config.destination_id,
                                          text=message_text + "*sticker*",
                                          parse_mode=PARSE_MODE)

    elif msg_attachment.type == "photo":
        source = max(msg_attachment.photo.sizes, key=lambda size: size.width)
        response = await bot.send_photo(chat_id=data_config.destination_id,
                                        caption=message_text,
                                        photo=source.url,
                                        parse_mode=PARSE_MODE)
    elif msg_attachment.type == "audio_message":
        response = await bot.send_voice(chat_id=data_config.destination_id,
                                        caption=message_text,
                                        voice=msg_attachment.audio_message.link_ogg,
                                        parse_mode=PARSE_MODE)
    else:
        doc = types.InputFile.from_url(url=msg_attachment.doc.url,
                                       filename=msg_attachment.doc.title)
        response = await bot.send_document(chat_id=data_config.destination_id,
                                           caption=message_text,
                                           document=doc,
                                           parse_mode=PARSE_MODE)
    return response
