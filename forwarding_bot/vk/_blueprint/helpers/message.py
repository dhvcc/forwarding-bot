from asyncio import sleep
from typing import List

from vkbottle.api import API
from vkbottle.bot import Message
from vkbottle.types.objects.messages import MessageAttachment
from vkbottle.types.objects.users import UserXtrCounters


class MessageHelper:
    @staticmethod
    def get_name(user: UserXtrCounters):
        return f"<em>{user.last_name} {user.first_name}</em>"

    @staticmethod
    def get_text(text: str):
        return f"<strong>{text[:1000]}</strong>"

    @staticmethod
    def get_valid_attachments(message: Message) -> List[MessageAttachment]:
        return [
            attach
            for attach in message.attachments
            if attach.type in ("photo", "doc", "sticker", "audio_message")
        ]

    @staticmethod
    async def get_sender(token: str, message: Message) -> UserXtrCounters:
        api = API(token)
        user_list = await api.users.get(user_ids=str(message.from_id))
        await sleep(0.1)
        return user_list[0]
