import logging
from asyncio import sleep
from typing import Dict
from typing import List

import aiohttp
import ujson
from vkbottle.api import API
from vkbottle.bot import Blueprint
from vkbottle.bot import Message
from vkbottle.types.objects.docs import Doc

from ..config.tg import BOT_TOKEN
from ..config.tg import DESTINATION_CONVERSATION_ID as DCI
from ..config.vk import GROUP_TOKEN

logger = logging.getLogger()

bot_bp = Blueprint()

api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/"
message_text_template = "<em>{sender}</em>:\n" \
                        "<strong>{text}</strong>"
parse_mode = "HTML"


class BadVibeException(Exception):
    """Doctype not allowed"""

    def __str__(self):
        return "Поддерживаются только документы .pdf или .gif"


class Utils:
    @staticmethod
    def get_valid_attachments(message: Message):
        return [attach for attach in message.attachments if attach.type in ("photo", "doc")]

    @staticmethod
    async def get_sender(token: str, message: Message):
        api = API(token)
        user_list = await api.users.get(user_ids=str(message.from_id))
        await sleep(0.1)
        return user_list[0]

    @staticmethod
    def format_message(sender, message: Message):
        return message_text_template.format(sender=f"{sender.last_name} {sender.first_name}",
                                            text=message.text)[:1000]

    @staticmethod
    def basic_params():
        return {
            "random_id": bot_bp.extension.random_id(),
            "chat_id": DCI,
            "parse_mode": parse_mode
        }

    @staticmethod
    async def vibe_check(response):
        if response.status < 300:
            logging.info(response.status)
            response.close()
            return True
        else:
            logging.warning(response.status)
            logging.warning(await response.text())
            response.close()
            return False


class AttachmentHandlers:
    @staticmethod
    async def no_attachments(session, request_params, tg_message):
        request_params["text"] = tg_message
        response = await session.get(api_url + "sendMessage", params=request_params)

        await Utils.vibe_check(response)

    @staticmethod
    async def one_attachment(session, request_params, attachments, tg_message):
        if attachments[0].type == "photo":
            photo = attachments[0].photo
            source = max(photo.sizes, key=lambda size: size.width)
            request_params["photo"] = source.url
            request_params["caption"] = tg_message
            response = await session.get(api_url + "sendPhoto", params=request_params)
            await Utils.vibe_check(response)
        else:
            doc = attachments[0].doc
            request_params["document"] = doc.url
            request_params["caption"] = tg_message
            response = await session.get(api_url + "sendDocument", params=request_params)
            if await Utils.vibe_check(response) is False:
                raise BadVibeException

    @staticmethod
    async def more_attachments(session, request_params, attachments, tg_message):
        media: List[Dict[str, str]] = []
        documents: List[Doc] = []
        for attach in attachments:
            if attach.type == "photo":
                photo = attach.photo
                source = max(photo.sizes, key=lambda size: size.width)
                media.append({
                    "type": attach.type,
                    "media": source.url,
                    "parse_mode": parse_mode
                })
            else:
                documents.append(attach.doc)

        if media:
            media[0]["caption"] = tg_message
            request_params["media"] = ujson.dumps(media)
            response = await session.get(api_url + "sendMediaGroup", params=request_params)
            await sleep(0.1)
            await Utils.vibe_check(response)
        if documents:
            bad_vibe = False
            if not media:
                request_params["caption"] = tg_message
                request_params["document"] = documents[0].url
                response = await session.get(api_url + "sendDocument", params=request_params)
                if await Utils.vibe_check(response) is False:
                    bad_vibe = True
                documents = documents[1:]
                request_params.pop("caption")
            for doc in documents:
                request_params["document"] = doc.url
                await sleep(0.3)
                response = await session.get(api_url + "sendDocument", params=request_params)
                if await Utils.vibe_check(response) is False:
                    bad_vibe = True
            if bad_vibe:
                raise BadVibeException


@bot_bp.on.chat_message()
async def handler(message: Message) -> None:
    """Default handler that catches any message"""

    sender = await Utils.get_sender(GROUP_TOKEN, message)
    request_params = Utils.basic_params()
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
        except BadVibeException as e:
            await message(str(e))
    await sleep(0.1)
