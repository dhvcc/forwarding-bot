import logging
from typing import Union

from aiohttp import ClientSession, FormData
from vkbottle.bot import Blueprint
from vkbottle.bot import Bot
from vkbottle.types.objects.docs import Doc

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
    async def send_document(cls, session, doc: Doc, params: dict):
        params = params.copy()
        document = await cls.get_document(doc)
        logger.debug(f"Sending document {document[:5]}...")
        data = FormData(quote_fields=False)
        data.add_field('document',
                       document,
                       filename=doc.title)
        return await session.post(api_url + "sendDocument", params=params, data=data)
