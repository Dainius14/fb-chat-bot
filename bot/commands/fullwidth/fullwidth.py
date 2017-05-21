from command import Command
from consts import *
import utils

class FullwidthCmd(Command):
    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        super().__init__()

    def execute(self, cmd_name, args, author_id):
        if args is None:
            self.sendMessage(self.config[Cmd.TXT_ARG_ERROR])

        args = utils.unicode_decode(args)
        msg = ""

        for i in args:
            # Space doesn't convert well
            if i == " ":
                msg += u"　"
            elif i == "\n":
                msg += u"\n"
            else:
                msg += chr(0xFEE0 + ord(i))

        self.sendMessage(msg)


def getObj():
    return FullwidthCmd()
