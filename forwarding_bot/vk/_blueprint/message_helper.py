from asyncio import sleep
from datetime import datetime
from typing import List, Optional, Union

from vkbottle.api import API
from vkbottle.types.objects.messages import MessageAttachment, ForeignMessage
from vkbottle.types.objects.users import UserXtrCounters
from vkbottle.types.objects.video import Video
from vkbottle.types.objects.wall import Wallpost
from vkbottle.user import Message

from forwarding_bot.settings import MINSK_TZ


class MessageHelper:

    @classmethod
    def get_date(cls, message: Union[Message, ForeignMessage]) -> str:
        dt = datetime.fromtimestamp(message.date)
        now = datetime.now(tz=MINSK_TZ)
        if now.date() != dt.date():
            return f"{dt.month}.{dt.day}.{dt.year}"
        return ""

    @staticmethod
    def get_name(user: UserXtrCounters) -> str:
        return f"{user.last_name} {user.first_name}"

    @classmethod
    def get_header(cls, user: UserXtrCounters, message: Union[Message, ForeignMessage]) -> str:
        date = cls.get_date(message)
        if date:
            return f"<em>{cls.get_name(user)}, {date}</em>"
        return f"<em>{cls.get_name(user)}</em>"

    @staticmethod
    def get_text(text: str) -> str:
        return f"<strong>{text[:1000]}</strong>"

    @staticmethod
    def get_valid_attachments(message: Union[Message, ForeignMessage]) -> List[MessageAttachment]:
        return [
            attach
            for attach in message.attachments
            if attach.type in ("photo", "video", "doc", "sticker", "audio_message", "wall")
        ]

    @staticmethod
    def is_link_attachment(attachment: MessageAttachment) -> bool:
        return attachment.type in ("video", "wall")

    @staticmethod
    def filter_media(attachments: List[MessageAttachment]) -> List[MessageAttachment]:
        return [
            attach
            for attach in attachments
            if attach.type in ("photo", "video")
        ]

    @staticmethod
    async def get_sender(token: Optional[str], message: Union[Message, ForeignMessage]) -> UserXtrCounters:
        api = API(token)
        user_list = await api.users.get(user_ids=str(message.from_id))
        await sleep(0.1)
        return user_list[0]

    @staticmethod
    def get_attachment_link(attachment: MessageAttachment) -> str:
        types = {
            "video": {
                "name": "видео",
                "getter": lambda x: x.video
            },
            "wall": {
                "name": "пост",
                "getter": lambda x: x.wall
            },
        }
        name = types[str(attachment.type)]["name"]
        getter = types[str(attachment.type)]["getter"]
        data: Union[Video, Wallpost] = getter(attachment)
        owner_id = getattr(data, 'owner_id', None) or getattr(data, 'from_id', None)
        url = f"vk.com/{attachment.type}{owner_id}_{data.id}" \
              f"?access_key={data.access_key or ''}"
        return f"[Вложение {name}: {url}]"
