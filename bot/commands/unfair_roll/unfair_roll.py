import random

from command import Command
from consts import *


class UnfairRollCmd(Command):
    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        super().__init__()

    def execute(self, cmd_name, args, author_id):
        unfair_list = []
        for key, value in self.config["rolls"].items():
            unfair_list += [key] * int(value)
        msg = random.choice(unfair_list)
        self.sendMessage(msg)


def getObj():
    return UnfairRollCmd()
