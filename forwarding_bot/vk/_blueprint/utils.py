import logging
from asyncio import sleep
from typing import List, Union

from aiohttp import ClientSession, FormData
from vkbottle.api import API
from vkbottle.bot import Blueprint
from vkbottle.bot import Message, Bot
from vkbottle.types.objects.docs import Doc
from vkbottle.types.objects.messages import MessageAttachment
from vkbottle.types.objects.users import UserXtrCounters

from forwarding_bot.config import data_config
from .settings import message_text_template, parse_mode, api_url

logger = logging.getLogger("forwarding-bot")


class BadDoctypeError(Exception):
    """Doctype not allowed exception"""

    def __str__(self):
        return "Поддерживаются только документы, фото и стикеры"


def get_valid_attachments(message: Message) -> List[MessageAttachment]:
    return [
        attach
        for attach in message.attachments
        if attach.type in ("photo", "doc", "sticker", "audio_message")
    ]


async def get_sender(token: str, message: Message) -> UserXtrCounters:
    api = API(token)
    user_list = await api.users.get(user_ids=str(message.from_id))
    await sleep(0.1)
    return user_list[0]


def format_message(sender, message: Message, text=None) -> str:
    return message_text_template.format(sender=f"{sender.last_name} {sender.first_name}",
                                        text=message.text if not text else text)[:1000]


def basic_params(bot: Union[Bot, Blueprint]) -> dict:
    return {
        "random_id": bot.extension.random_id(),
        "chat_id": data_config.destination_id,
        "parse_mode": parse_mode
    }


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


async def get_document(doc: Doc) -> bytes:
    async with ClientSession() as session:
        document_response = await session.get(doc.url)
        return await document_response.content.read()


async def send_document(session, doc: Doc, params: dict):
    params = params.copy()
    document = await get_document(doc)
    logger.debug(f"Sending document {document[:5]}...")
    data = FormData(quote_fields=False)
    data.add_field('document',
                   document,
                   filename=doc.title)
    return await session.post(api_url + "sendDocument", params=params, data=data)
