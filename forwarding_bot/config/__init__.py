import ujson

config = {}

if not config:
    with open("config.json") as file:
        config = ujson.loads(file.read())
