class ArgsModel:
    """Argparse output namespace schema to make linters work"""
    bot_token: str
    user_token: str
    destination_id: str
    source_id: str
    limited_attachments: bool
