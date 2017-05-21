from command import SuperCommand
from consts import *


class HelpCmd(SuperCommand):
    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        super().__init__()

    def execute(self, cmd_name, args, author_id):
        response = ""
        for cmd in self._bot.commands:
            if not cmd.config[Cmd.NAME] or cmd.config[Cmd.IS_ADMIN]:
                continue
            response += "{0}".format(cmd.config[Cmd.NAME])
            response += " ({0})".format(cmd.config[Cmd.ALT_NAME]) if cmd.config[Cmd.ALT_NAME] else ""
            response += " - {0}\n".format(cmd.config[Cmd.INFO])
        self.sendMessage(response)


def getObj():
    return HelpCmd()
