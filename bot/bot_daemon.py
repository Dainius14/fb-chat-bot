import logging
import json
import daemon

import bot


my_bot = None
try:
    with open("../config.json", encoding="utf-8") as infile:
        config = json.load(infile)
        my_bot = bot.FbChatBot(config)
except IOError as e:
    logging.exception("Can't open file config.json", e)
    exit(1)

with daemon.DaemonContext():
    my_bot.startListening()

logging.info("Bot started.")
