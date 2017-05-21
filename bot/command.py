import json
import os
from abc import abstractmethod

from consts import Cmd


class Command:
    def __init__(self):
        self.is_loaded = False
        self.sendMessage = None

        try:
            dirpath = "{0}\\commands\\{1}\\".format(os.path.dirname(os.path.realpath(__file__)), self.module_name)

            with open(dirpath + self.module_name + ".json", encoding="utf-8") as infile:
                self.config = json.load(infile)

                self.name = self.config[Cmd.NAME]
                self.alt_name = self.config[Cmd.ALT_NAME]

                self.is_loaded = True
        except IOError as e:
            print("Can't open config file: " + str(e))

    def init(self, send_message):
        self.sendMessage = send_message

    @abstractmethod
    def execute(self, cmd_name, args, author_id):
        raise NotImplementedError

    def isAdminCommand(self):
        return self.config[Cmd.IS_ADMIN]

    def checkCommand(self, input_text):
        return input_text in [self.config[Cmd.NAME], self.config[Cmd.ALT_NAME]]


class SuperCommand(Command):
    def init(self, send_message, bot):
        super().init(send_message)
        self._bot = bot

