import random

from command import Command
from consts import *


class RollCmd(Command):
    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        super().__init__()

    def execute(self, cmd_name, args, author_id):
        try:
            n = int(args or "")
            response = str(random.randint(0, n))
        except ValueError:
            response = self.config[Cmd.TXT_ARG_ERROR]
        self.sendMessage(response)


def getObj():
    return RollCmd()
