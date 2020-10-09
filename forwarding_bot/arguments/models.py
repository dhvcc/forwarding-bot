class ArgsModel:
    """Argparse output namespace schema to make linters work"""
    bot_token: str
    group_token: str
    destination_id: str
    source_id: str
