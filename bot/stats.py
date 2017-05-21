import io
import json
import time
import threading
import shutil
import os


class Stats:
    """Manages stats file"""


    # def updateCommandsExecuted(self, name_code, command):
    #     self.vals["commands_executed"] += 1
    #
    #     cmd = self.vals["commands"].get(command)
    #     if cmd:
    #         cmd["count"] += 1
    #         cmd["last_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #
    #         for item in cmd["by_user"]:
    #             val = item.get(name_code)
    #             if val:
    #                 item[name_code] += 1
    #                 break
    #         # First time executed by user
    #         else: cmd["by_user"].append({ name_code : 1 })
    #
    #     # First time executed
    #     # else:
    #     #     self.vals["commands"][command] = { "count" : 1 }
    #     #     self.vals["commands"][command]["last_time"] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    #     #     self.vals["commands"][command]["by_user"] = [{ name_code : 1 }]
    #
    #     self.makeDirty()

    def updateCommandsError(self):
        self.vals["commands_error"] += 1
        self.makeDirty()

    def updateMessagesSent(self):
        self.vals["messages_sent"] += 1
        self.makeDirty()


