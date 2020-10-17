from forwarding_bot.vk import VKBot
from forwarding_bot.config import data_config


# Feature
# TODO: Add reply message support (only text)
# TODO: Add nested media group splitter to send photos in media groups

# Refactor
# TODO: Create bot instances in init, so other can access them. And close tg bot in the end of main
# TODO: add verbose logging and file logging
# TODO: Rewrite using vkbottle v3.0

def main():
    bot = VKBot(token=data_config.user_token)
    bot.start()


if __name__ == "__main__":
    main()
