import json
import os

from command import SuperCommand
from consts import *


class SaveUsersCmd(SuperCommand):
    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        super().__init__()

    def execute(self, cmd_name, args, author_id):
        # Extracts ids from participants and gets full data

        threads = self._bot.getThreadList(0)
        thread = []
        for key in threads:
            if key.thread_fbid == self._bot.config["thread_id"]:
                thread = key
                break
        else:
            return

        users = []
        for user_id in thread.participants:
            if user_id.startswith("fbid:"):
                users.append(user_id[5:])

        full_users = []
        for user in users:
            full_users.append(self._bot.getUserInfo(user))

        for user in full_users:
            # User is not in config
            user_id = user["id"]
            if user_id not in list(self._bot.config[USERS].keys()):
                new_user = {
                    User.NAME: user["firstName"],
                    User.FULL_NAME: user["name"],
                    User.GENDER: user["gender"],
                    User.URL: user["uri"],
                    User.IN_CHAT: True,
                    User.IS_FRIEND: user["is_friend"],
                    User.NICKNAMES: [],
                    User.ADDRESSING_NAMES: []}
                self._bot.config[USERS][user_id] = new_user

        # User is in config, but not in chat
        for key, val in self._bot.config[USERS].items():
            for user in full_users:
                if key == user["id"]:
                    break
            else:
                self._bot.config[USERS][key][User.IN_CHAT] = False

        mypath = os.path.dirname(os.path.realpath(__file__))

        with open(os.path.join(mypath, "../../../config.json"), "w", encoding="utf-8") as outfile:
            json.dump(self._bot.config, outfile, indent="\t", ensure_ascii=False)

        self.sendMessage(self.config[Cmd.TXT_EXECUTED])


def getObj():
    return SaveUsersCmd()
