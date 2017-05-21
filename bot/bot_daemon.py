import logging
import json
import daemon

import bot

context = daemon.DaemonContext(
    working_directory='/home/pi/fb-chat-bot/bot',
    )

config = None
stats = None
try:
    with open("../config.json", encoding="utf-8") as infile:
        config = json.load(infile)
    with open("../stats.json", encoding="utf-8") as infile:
        stats = json.load(infile)
except IOError as e:
    logging.exception("Can't open file config.json", e)
    exit(1)

my_bot = bot.FbChatBot(config, stats)
with context:
    my_bot.listen()
