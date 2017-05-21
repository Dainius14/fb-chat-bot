import json
from urllib import request
import requests
from lxml import html

from command import Command
from consts import *


class UrbanDictionaryCmd(Command):
    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        super().__init__()

    def execute(self, cmd_name, args, author_id):
        if args is None:
            self.sendMessage(self.config[Cmd.TXT_ARG_ERROR])

        args = args.replace(" ", "+")
        url = "http://api.urbandictionary.com/v0/define?term=" + args

        response = json.load(request.urlopen(url))

        # Page not found
        if response["result_type"] == "no_results":
            self.sendMessage(self.config[Cmd.TXT_ERROR])
            return

        msg = ""
        for i in range(2):
            result = response["list"][i]
            word = result["word"]
            definition = result["definition"]
            example = result["example"]

            msg += self.config[Cmd.TXT_EXECUTED].format((i + 1), word, definition, example)

        msg += response["list"][0]["permalink"]

        self.sendMessage(msg)


def getObj():
    return UrbanDictionaryCmd()
