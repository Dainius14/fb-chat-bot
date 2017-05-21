from command import Command
from consts import *


class OneLinersCmd(Command):
    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        super().__init__()

    def execute(self, cmd_name, args, author_id):
        self.sendMessage(self.config["one_liners"].get(cmd_name, ""))

    def checkCommand(self, input_text):
        return input_text in list(self.config["one_liners"].keys())


def getObj():
    return OneLinersCmd()
