from vkbottle.bot import Blueprint, Message
from vkbottle.ext import Middleware

from forwarding_bot.config import data_config

middleware_bp = Blueprint()


@middleware_bp.middleware.middleware_handler()
class ValidChatMiddleware(Middleware):
    """A middleware that skips messages to other chats"""

    async def pre(self, message: Message, *args):
        if message.chat_id != data_config.source_id:
            return False


@middleware_bp.middleware.middleware_handler()
class NoTextMiddleware(Middleware):
    """A middleware that skips empty messages i.e. kicks, invites and other"""

    async def pre(self, message: Message, *args):
        if not message.text and not message.attachments and not message.fwd_messages and not message.reply_message:
            return False
