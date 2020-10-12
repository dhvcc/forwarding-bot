import logging
from typing import Union, List

from aiohttp import ClientSession, FormData
from vkbottle.bot import Blueprint
from vkbottle.bot import Bot
from vkbottle.types.objects.docs import Doc
from vkbottle.types.objects.photos import Photo
from vkbottle.types.objects.messages import AudioMessage, MessageAttachment

from forwarding_bot.config import data_config
from ..settings import parse_mode, api_url

logger = logging.getLogger("forwarding-bot")


class BadDoctypeError(Exception):
    """Doctype not allowed exception"""

    def __str__(self):
        return "Поддерживаются только документы, фото и стикеры"


class RequestHelper:
    @staticmethod
    def get_params(bot: Union[Bot, Blueprint]) -> dict:
        return {
            "random_id": bot.extension.random_id(),
            "chat_id": data_config.destination_id,
            "parse_mode": parse_mode
        }

    @staticmethod
    async def response_check(response) -> bool:
        if response.status < 300:
            logger.debug(response.status)
            response.close()
            return True
        else:
            logger.warning(f"Bad response status {response.status}")
            logger.warning(await response.text())
            response.close()
            return False

    @staticmethod
    async def get_document(doc: Doc) -> bytes:
        async with ClientSession() as session:
            document_response = await session.get(doc.url)
            return await document_response.content.read()

    @classmethod
    async def send_photo(cls, session, photo: Photo, params: dict):
        params = params.copy()
        source = max(photo.sizes, key=lambda size: size.width)
        params["photo"] = source.url
        logger.debug("Sending photo")
        return await session.get(api_url + "sendPhoto", params=params)

    @classmethod
    async def send_media_group(cls, session, attachments: List[MessageAttachment], params: dict):
        pass
        # params = params.copy()
        # media = MessageHelper.filter_media(attachments)
        # TODO: filter separate captions
        # logger.debug(f"Sending media group")
        # return await session.get(api_url + "sendMediaGroup", params=params)

    @classmethod
    async def send_voice(cls, session, voice: AudioMessage, params: dict):
        params = params.copy()
        params["voice"] = voice.link_ogg
        logger.debug("Sending voice message")
        return await session.get(api_url + "sendVoice", params=params)

    @classmethod
    async def send_document(cls, session, doc: Doc, params: dict):
        params = params.copy()
        document = await cls.get_document(doc)
        logger.debug(f"Sending document {document[:5]}...")
        data = FormData(quote_fields=False)
        data.add_field('document',
                       document,
                       filename=doc.title)
        return await session.post(api_url + "sendDocument", params=params, data=data)
