from forwarding_bot.config import data_config

api_url = f"https://api.telegram.org/bot{data_config.bot_token}/"
message_text_template = "<em>{sender}</em>:\n" \
                        "<strong>{text}</strong>"
parse_mode = "HTML"
