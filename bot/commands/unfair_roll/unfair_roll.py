import random

from command import Command
from consts import *


class UnfairRollCmd(Command):
    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        super().__init__()

    def execute(self, cmd_name, args, author_id):
        response = random.choices(list(self.config["rolls"].keys()), list(self.config["rolls"].values()))
        self.sendMessage(response)


def getObj():
    return UnfairRollCmd()
