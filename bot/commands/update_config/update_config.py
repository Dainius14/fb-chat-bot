import json
import os

from command import SuperCommand
from consts import *


class UpdateConfigCmd(SuperCommand):
    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        super().__init__()

    def execute(self, cmd_name, args, author_id):
        mypath = os.path.dirname(os.path.realpath(__file__))

        with open(os.path.join(mypath, "../../../config.json"), encoding="utf-8") as infile:
            new_config = json.load(infile)
        self._bot.config.update(new_config)
        self.sendMessage(self.config[Cmd.TXT_EXECUTED])


def getObj():
    return UpdateConfigCmd()
