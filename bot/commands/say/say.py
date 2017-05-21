from command import Command
from consts import *


class SayCmd(Command):
    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        super().__init__()

    def execute(self, cmd_name, args, author_id):
        if args is None or len(args) == 0:
            self.sendMessage(self.config[Cmd.TXT_ARG_ERROR])
            return

        self.sendMessage(args)


def getObj():
    return SayCmd()
