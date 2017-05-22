import random

from command import Command
from consts import *


class MagicBallCmd(Command):
    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        super().__init__()

    def execute(self, cmd_name, args, author_id):
        msg = random.choice(self.config["answers"])
        self.sendMessage(msg)


def getObj():
    return MagicBallCmd()
