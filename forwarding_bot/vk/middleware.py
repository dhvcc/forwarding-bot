from vkbottle.bot import Blueprint
from vkbottle.bot import Message
from vkbottle.ext import Middleware

from ..config.vk import SOURCE_CONVERSATION_ID as SCI

middleware_bp = Blueprint()


@middleware_bp.middleware.middleware_handler()
class ValidChatMiddleware(Middleware):
    """A middleware that skips messages to other chats"""

    async def pre(self, message: Message, *args):
        if message.from_chat and message.chat_id != SCI:
            return False


@middleware_bp.middleware.middleware_handler()
class NoTextMiddleware(Middleware):
    """A middleware that skips empty messages i.e. invites, stickers, ..."""

    async def pre(self, message: Message, *args):
        if not message.text and not message.attachments:
            return False
