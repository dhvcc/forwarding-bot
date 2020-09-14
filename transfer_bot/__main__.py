import logging

from vkbottle import Bot

from transfer_bot.blueprint import bot_bp
from transfer_bot.config.vk import GROUP_TOKEN
from transfer_bot.middleware import middleware_bp

logger = logging.getLogger()


class TransferBot:
    def __init__(self):
        self.bot = Bot(GROUP_TOKEN, debug="DEBUG")
        self.bot.set_blueprints(middleware_bp, bot_bp)

    def start(self) -> None:
        try:
            self.bot.run_polling()
        except Exception as e:
            logger.exception(f"Transfer bot crashed with {str(e)}")


if __name__ == "__main__":
    bot = TransferBot()
    bot.start()
