import re

from command import Command
from consts import *
import utils


class FullwidthSquareCmd(Command):
    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        super().__init__()

    def execute(self, cmd_name, args, author_id):
        if args is None:
            self.sendMessage(self.config[Cmd.TXT_ARG_ERROR])

        def toFullwidth(char):
            # Space doesn't convert well
            if char == " ":
                return u"　"
            elif char == "\n":
                return u"\n"
            else:
                return chr(0xFEE0 + ord(char))

        args = utils.unicode_decode(args)
        msg = ""

        for i in args:
            msg += toFullwidth(i)

        for i, letter in enumerate(args[1:-1:]):
            msg += "\n" + toFullwidth(letter)
            msg += ' ' * int(3.7 * (len(args) - 2))  # Every letter occupies 3.7 space letters
            msg += ' ' * len(re.findall(' +', args[1:-1:]))  # Extra letter for each space in word
            msg += toFullwidth(args[-(i + 2)])

        msg += "\n"
        for i in args[::-1]:
            msg += toFullwidth(i)

        self.sendMessage(msg)


def getObj():
    return FullwidthSquareCmd()
