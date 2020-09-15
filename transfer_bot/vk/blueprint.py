import logging
from asyncio import sleep

import aiohttp
import ujson
from vkbottle.api import API
from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from transfer_bot.config.tg import BOT_TOKEN
from transfer_bot.config.tg import DESTINATION_CONVERSATION_ID as DCI
from transfer_bot.config.vk import GROUP_TOKEN

logger = logging.getLogger()

bot_bp = Blueprint()

api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/"
tg_photo_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
message_text_template = "{sender}:\n" \
                        "{text}"


def get_valid_attachments(message: Message):
    return [attach for attach in message.attachments if attach.type in ("photo",)]


async def get_sender(token: str, message: Message):
    api = API(token)
    user_list = await api.users.get(user_ids=str(message.from_id))
    await sleep(0.1)
    return user_list[0]


def format_message(sender, message: Message):
    return message_text_template.format(sender=f"{sender.last_name} {sender.first_name}",
                                        text=message.text)[:1000]


def basic_params():
    return {
        "random_id": bot_bp.extension.random_id(),
        "chat_id": DCI
    }


async def no_attachments(session, request_params, tg_message):
    request_params["text"] = tg_message
    response = await session.get(api_url + "sendMessage", params=request_params)

    return response


async def one_attachment(session, request_params, attachments, tg_message):
    photo = attachments[0].photo
    source = max(photo.sizes, key=lambda size: size.width)
    request_params["photo"] = source.url
    request_params["caption"] = tg_message
    response = await session.get(api_url + "sendPhoto", params=request_params)

    return response


async def more_attachments(session, request_params, attachments, tg_message):
    request_params["media"] = []
    for attach in attachments:
        photo = attach.photo
        source = max(photo.sizes, key=lambda size: size.width)
        request_params["media"].append({
            "type": attach.type,
            "media": source.url,
        })
        request_params["media"][0]["caption"] = tg_message
    request_params["media"] = ujson.dumps(request_params["media"])
    response = await session.get(api_url + "sendMediaGroup", params=request_params)

    return response


@bot_bp.on.chat_message()
async def handler(message: Message) -> None:
    """Default handler that catches any message"""

    sender = await get_sender(GROUP_TOKEN, message)
    request_params = basic_params()
    tg_message = format_message(sender, message)
    attachments = get_valid_attachments(message)

    async with aiohttp.ClientSession() as session:
        if not attachments:
            response = await no_attachments(session, request_params, tg_message)
        elif len(attachments) == 1:
            response = await one_attachment(session, request_params, attachments, tg_message)
        else:
            response = await more_attachments(session, request_params, attachments, tg_message)
        # Response vibe check
        if response.status < 300:
            logging.info(response.status)
        else:
            logging.warning(response.status)
            logging.warning(await response.text())
        response.close()
        await sleep(0.1)
