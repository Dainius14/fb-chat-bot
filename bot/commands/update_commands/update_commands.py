import importlib
import json
import os

from command import SuperCommand
from consts import *


class UpdateCommandsCmd(SuperCommand):
    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        super().__init__()

    def execute(self, cmd_name, args, author_id):
        self._bot.loadCommands(True)
        self.sendMessage(self.config[Cmd.TXT_EXECUTED])


def getObj():
    return UpdateCommandsCmd()
