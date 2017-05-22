import random
from urllib import request

from command import Command
from consts import *
from utils import *


class NumbersApiCmd(Command):
    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        super().__init__()

    def execute(self, cmd_name, args, author_id):
        number = "random"
        ttype = random.choice(self.config["types"])

        if args:
            args = args.split()
            if len(args) == 1:
                if isInt(args[0]):
                    number = args[0]
                    ttype = random.choice(self.config["types"])
                elif len(args[0].split("/")) == 2:
                    number = args[0]
                    ttype = "date"
                elif args[0].lower() in self.config["types"]:
                    number = "random"
                    ttype = args[0].lower()

            if len(args) == 2:
                number = args[0]
                ttype = args[1]

        msg = request.urlopen("http://numbersapi.com/{0}/{1}".format(number, ttype))

        self.sendMessage(msg)


def getObj():
    return NumbersApiCmd()
