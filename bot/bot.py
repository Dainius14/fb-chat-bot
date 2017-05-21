import json
import os
import random
import re
import shutil
import threading

import time

from fbchat.client import Client as fbchat
from fbchat.models import *
from consts import *

import importlib
import logging


class FbChatBot(fbchat):
    def __init__(self, config, stats):
        """
        Set up bot.

        :param email: email to login with 
        :param password: password to use
        :param config: config file to use
        :param stats: stats file to use
        """

        # Setup bot
        self.config = config
        self.stats = stats
        self.cmsgs = config["messages"]
        self.commands = {}
        self.loadCommands(False)

        # Init fbchat
        fbchat.__init__(self, config["email"], config["password"], logging_level=logging.INFO, do_login=True)
        thread_type = ThreadType.USER if config["is_thread_user"] else ThreadType.GROUP
        self.setDefaultThread(config["thread_id"], thread_type)

        # Setup events
        self.onListening += lambda: self.sendMessage(self.cmsgs[Msgs.ON_LOGGED_IN])
        self.onMessage += self._onMessage

        # Setup stats
        self.is_stats_dirty = False
        self.last_stats_update = time.time()
        self.stats["times_launched"] += 1
        self.stats["current_uptime"] = 0
        self.updateStats()

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

        self.commands["quiz"].tryGuess(author_id, message)

    def getCommandObj(self, command_name):
        """Returns a dict of given command.py with all related info. None if command.py not found"""
        for command in self.commands.values():
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
                self.commands[dirname] = obj

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

    def fbidToName(self, fbid: str) -> str:
        user = self.config[USERS].get(fbid)
        if user is None:
            return None
        return user["name"]

    def updateStats(self):
        """Every 10s writes to stats file new updates, if there are any"""
        threading.Timer(30, self.updateStats).start()

        # Keeps track of uptime
        diff = time.time() - self.last_stats_update
        if diff >= 60:
            self.stats["uptime_minutes"] += 1
            self.stats["current_uptime"] += 1
            self.is_stats_dirty = True
            self.last_stats_update = time.time()

        # Writes only if data is modified
        if self.is_stats_dirty:
            shutil.copyfile("../stats.json", "../stats.tmp.json")
            try:
                with open("../stats.json", "w", encoding="utf-8") as outfile:
                    json.dump(self.stats, outfile, indent="\t", ensure_ascii=False)
            except IOError as e:
                shutil.copyfile("../stats.tmp.json", "../stats.json")

            self.is_stats_dirty = False

    def markStatsDirty(self):
        self.is_stats_dirty = True
