import json
from urllib import request
import requests
from lxml import html

from command import Command
from consts import *


class WikipediaCmd(Command):
    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        super().__init__()

    def execute(self, cmd_name, args, author_id):
        if args is None:
            self.sendMessage(self.config[Cmd.TXT_ARG_ERROR])

        args = args.replace(" ", "_")
        url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles="
        url += args

        response = json.load(request.urlopen(url))

        extract = response["query"]["pages"]

        # Page not found
        if "-1" in extract:
            self.sendMessage(Cmd.TXT_ERROR)
            return

        extract = next(iter(extract.values()))

        url_to_add = "https://en.wikipedia.org/wiki/" + args
        msg = extract["extract"] + "\n" + url_to_add

        self.sendMessage(msg)


def getObj():
    return WikipediaCmd()
