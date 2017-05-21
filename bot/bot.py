import os
import random
import re

from fbchat.client import Client as fbchat
from fbchat.models import *
from consts import *

import importlib
import logging


class FbChatBot(fbchat):
    def __init__(self, config):
        """
        Set up bot.

        :param email: email to login with 
        :param password: password to use
        :param config: config file to use
        :param stats: stats file to use
        """

        # Setup bot
        self.config = config
        self.cmsgs = config["messages"]
        self.commands = []
        self.loadCommands(False)

        # Init fbchat
        fbchat.__init__(self, config["email"], config["password"], logging_level=logging.INFO, do_login=True)
        thread_type = ThreadType.USER if config["is_thread_user"] else ThreadType.GROUP
        self.setDefaultThread(config["thread_id"], thread_type)

        # Setup events
        self.onListening += lambda: self.sendMessage(self.cmsgs[Msgs.ON_LOGGED_IN])
        self.onMessage += self._onMessage

    def startListening(self):
        self.listen()

    def _onMessage(self, mid, author_id, message, thread_id, thread_type, ts, metadata):
        """ Routes incoming messages. """

        # Message from myself, ignore
        if author_id == self.uid:
            return

        # Mark received message as delivered and seen
        self.markAsDelivered(mid, thread_id)
        self.markAsRead(thread_id, ts + 100)

        # Message from somewhere I'm not listening
        if thread_id != self.config["thread_id"]:
            return

        # Message is from my group, do my bot things

        is_command = False
        # Commands
        if message.startswith("!"):
            parts = message.split(" ", 1)
            command_name = parts[0].lower()
            command_args = parts[1] if len(parts) == 2 else None

            command = self.getCommandObj(command_name)

            # It's a command
            if command:
                # Admin only command.py
                if command.isAdminCommand() and author_id not in self.config[ADMIN_FBID_LIST]:
                    self.sendMessage(self.cmsgs[Msgs.CMD_ERROR_NOT_ADMIN])

                try:
                    command.execute(command_name, command_args, author_id)
                except Exception as e:
                    self.sendMessage(self.cmsgs[Msgs.CMD_ERROR_EXEC].format(str(e)))

                return

            # Not a command

        self.responderToText(author_id, message)

    def getCommandObj(self, command_name):
        """Returns a dict of given command.py with all related info. None if command.py not found"""
        for command in self.commands:
            if command.checkCommand(command_name):
                return command

    def loadCommands(self, reload):
        self.commands.clear()
        for dirname in os.listdir("./commands"):
            full_dir = "./commands/" + dirname
            if not os.path.isdir(full_dir):
                continue

            filename = full_dir + "/" + dirname + ".py"
            if not os.path.exists(filename):
                print(dirname + " does not exist or some shit")
                continue

            module_name = "commands.{0}.{0}".format(dirname)

            mod = importlib.import_module(module_name)
            if reload:
                mod = importlib.reload(mod)

            obj = mod.getObj()

            from command import SuperCommand
            if isinstance(obj, SuperCommand):  # Give the bot itself if it's a super command
                obj.init(self.sendMessage, self)
            else:  # Regular command
                obj.init(self.sendMessage)

            if obj.is_loaded:
                self.commands.append(obj)

    def responderToText(self, author_id, message):
        """Checks if there are words matching respondable words in config, then responds."""

        items = self.config["responder"]
        matched = []

        # Finds matched items
        for item in items:
            for word in item["triggers"]:
                if re.search(word, message):  # Word found
                    if random.randint(0, 100) <= item["probability"]:  # Adds depending on the probability
                        matched.append(item)
                    break

        # No matches found
        if not matched:
            return

        trigger_set = random.choice(matched)
        answer = random.choice(trigger_set["answers"])

        self.sendMessage(answer)

    """
    Core commands for controlling vital stuff
    """

