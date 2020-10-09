import logging

from vkbottle import Bot

from forwarding_bot.config import data_config
from forwarding_bot.vk._middleware import middleware_bp
from ._blueprint import bot_bp

logger = logging.getLogger("forwarding-bot")


class VKBot:
    def __init__(self):
        self.bot = Bot(data_config.group_token, debug="DEBUG")
        self.bot.set_blueprints(middleware_bp, bot_bp)

    def start(self) -> None:
        logger.info("Starting VKBot")
        try:
            self.bot.run_polling(skip_updates=True)
        except Exception as e:
            logger.exception(f"VK bot crashed. {e}")
