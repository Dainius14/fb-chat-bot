import calendar
import datetime
import time

from command import Command
from consts import Cmd


class TimeCmd(Command):
    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        super().__init__()

    def execute(self, cmd_name, args, author_id):
        dtnow = datetime.datetime.now()
        local_time = time.localtime()

        msg = time.strftime(self.config[Cmd.TXT_FORMAT], local_time)
        cal = calendar.TextCalendar(calendar.MONDAY).formatmonth(dtnow.year, dtnow.month)
        cal = cal.replace("  ", "   ")
        cal = cal.replace("\n ", "\n  ")
        msg += cal

        self.sendMessage(msg)


def getObj():
    return TimeCmd()
