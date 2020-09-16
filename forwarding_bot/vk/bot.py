import logging

from vkbottle import Bot

from ..config.vk import GROUP_TOKEN
from ..vk.blueprint import bot_bp
from ..vk.middleware import middleware_bp

logger = logging.getLogger()


class VKBot:
    def __init__(self):
        self.bot = Bot(GROUP_TOKEN, debug="DEBUG")
        self.bot.set_blueprints(middleware_bp, bot_bp)

    def start(self) -> None:
        try:
            self.bot.run_polling(skip_updates=True)
        except Exception as e:
            logger.exception(f"VK bot crashed with {str(e)}")
