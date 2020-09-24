import logging
from asyncio import sleep

from vkbottle.api import API
from vkbottle.bot import Message

from forwarding_bot.config import data_config
from .settings import message_text_template, parse_mode


class BadRequestError(Exception):
    """Probably doctype not allowed"""

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
    def basic_params(bot):
        return {
            "random_id": bot.extension.random_id(),
            "chat_id": data_config.destination_id,
            "parse_mode": parse_mode
        }

    @staticmethod
    async def response_check(response):
        if response.status < 300:
            logging.info(response.status)
            response.close()
            return True
        else:
            logging.warning(response.status)
            logging.warning(await response.text())
            response.close()
            return False
