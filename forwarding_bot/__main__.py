from forwarding_bot.vk import VKBot


# TODO: Rewrite using vkbottle v3.0
# TODO: Use aiogram instead of plain aiohttp
# TODO: add verbose logging

# TODO: Add reply message support (only text)

def main():
    vk_bot = VKBot()
    vk_bot.start()


if __name__ == "__main__":
    main()
