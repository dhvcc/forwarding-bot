import logging
from asyncio import sleep

import aiohttp
from vkbottle.api import API
from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from transfer_bot.config.tg import BOT_TOKEN
from transfer_bot.config.tg import DESTINATION_CONVERSATION_ID as DCI
from transfer_bot.config.vk import GROUP_TOKEN

logger = logging.getLogger()

bot_bp = Blueprint()

tg_message_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
message_text_template = "{sender}:\n" \
                        "{text}"


@bot_bp.on.chat_message()
async def handler(message: Message) -> None:
    """Default handler that catches any message"""

    # Get sender info
    api = API(GROUP_TOKEN)
    user_list = await api.users.get(user_ids=str(message.from_id))
    await sleep(0.1)
    user = user_list[0]

    # Construct the message
    tg_message = message_text_template.format(sender=f"{user.last_name} {user.first_name}",
                                              text=message.text)
    if message.attachments:
        tg_message += f"\nВложений: {len(message.attachments)}"

    # Init get parameters
    request_params = {"no_webpage": 1,
                      "random_id": bot_bp.extension.random_id(),
                      "chat_id": DCI,
                      "text": tg_message}

    # Send
    async with aiohttp.ClientSession() as session:
        async with session.get(tg_message_url, params=request_params) as response:
            if response.status < 300:
                logging.info(response.status)
            else:
                logging.warning(response.status)
                logging.warning(await response.text())
        await sleep(0.1)
