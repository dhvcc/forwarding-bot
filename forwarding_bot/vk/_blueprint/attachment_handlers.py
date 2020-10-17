import logging

from aiogram import Bot, types
from vkbottle.types.objects.messages import MessageAttachment

from forwarding_bot.config import data_config

logger = logging.getLogger("forwarding-bot")


async def handle_attachment(
        bot: Bot,
        message_text: str,
        msg_attachment: MessageAttachment,
):
    logger.debug(f"One attachment with type {msg_attachment.type}")
    if msg_attachment.type == "sticker":
        await bot.send_message(chat_id=data_config.destination_id,
                               text=message_text + "*sticker*",
                               parse_mode=data_config.parse_mode)

    elif msg_attachment.type == "photo":
        source = max(msg_attachment.photo.sizes, key=lambda size: size.width)
        await bot.send_photo(chat_id=data_config.destination_id,
                             caption=message_text,
                             photo=source.url,
                             parse_mode=data_config.parse_mode)
    elif msg_attachment.type == "audio_message":
        await bot.send_voice(chat_id=data_config.destination_id,
                             caption=message_text,
                             voice=msg_attachment.audio_message.link_ogg,
                             parse_mode=data_config.parse_mode)
    else:
        doc = types.InputFile.from_url(url=msg_attachment.doc.url,
                                       filename=msg_attachment.doc.title)
        await bot.send_document(chat_id=data_config.destination_id,
                                caption=message_text,
                                document=doc,
                                parse_mode=data_config.parse_mode)
