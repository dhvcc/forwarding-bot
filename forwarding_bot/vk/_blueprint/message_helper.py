from asyncio import sleep
from typing import List
from datetime import datetime, timezone, timedelta
from vkbottle.api import API
from vkbottle.user import Message
from vkbottle.types.objects.messages import MessageAttachment
from vkbottle.types.objects.users import UserXtrCounters
import pytz


class MessageHelper:
    _utc3_offset = timedelta(hours=3)
    _utc3_zone = timezone(offset=_utc3_offset, name="UTC")
    _tz = pytz.timezone("Europe/Minsk")

    @classmethod
    def get_date(cls, message: Message) -> str:
        dt = datetime.fromtimestamp(message.date)
        now = datetime.now(tz=cls._tz)
        if now.date() != dt.date():
            return f"{dt.month}.{dt.day}.{dt.year} "
        return ""

    @staticmethod
    def get_name(user: UserXtrCounters) -> str:
        return f"{user.last_name} {user.first_name}"

    @classmethod
    def get_header(cls, user: UserXtrCounters, message: Message) -> str:
        date = cls.get_date(message)
        if date:
            return f"<em>{cls.get_name(user)}, {date}</em>"
        return f"<em>{cls.get_name(user)}</em>"

    @staticmethod
    def get_text(text: str) -> str:
        return f"<strong>{text[:1000]}</strong>"

    @staticmethod
    def get_valid_attachments(message: Message) -> List[MessageAttachment]:
        return [
            attach
            for attach in message.attachments
            if attach.type in ("photo", "doc", "sticker", "audio_message")
        ]

    @staticmethod
    def filter_media(attachments: List[MessageAttachment]) -> List[MessageAttachment]:
        return [
            attach
            for attach in attachments
            if attach.type in ("photo", "video")
        ]

    @staticmethod
    async def get_sender(token: str, message: Message) -> UserXtrCounters:
        api = API(token)
        user_list = await api.users.get(user_ids=str(message.from_id))
        await sleep(0.1)
        return user_list[0]