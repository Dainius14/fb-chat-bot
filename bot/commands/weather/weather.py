import random

import time

import requests
from lxml import html

from command import Command
from consts import *


class WeatherCmd(Command):
    def __init__(self):
        self.module_name = __name__.split(".")[-1]
        super().__init__()

    def execute(self, cmd_name, args, author_id):

        def getData(place_code):
            page = requests.get("http://www.meteo.lt/lt_LT/miestas?placeCode=" + place_code)
            tree = html.fromstring(page.content)
            td = tree.cssselect("div.weather_info.type_1")[0]
            temp_now = td.cssselect("span.temperature")[0].text
            if int(temp_now) > 0:
                temp_now = "+" + temp_now
            type_now = td.cssselect("span.large.condition")[0].get("title").lower()

            tmrw = tree.cssselect("div.portlet-body div.weather_block_city div.slider")[0].getchildren()[1]
            tmrw = tmrw.cssselect("a")[0].getchildren()
            tmrw_night_temp = tmrw[2][2].text[:-3]
            if int(tmrw_night_temp) > 0: tmrw_night_temp = "+" + tmrw_night_temp
            tmrw_night_type = tmrw[2][1].get("title").lower()
            tmrw_day_temp = tmrw[3][2].text[:-3]
            if int(tmrw_day_temp) > 0: tmrw_day_temp = "+" + tmrw_day_temp
            tmrw_day_type = tmrw[3][1].get("title").lower()
            return temp_now, type_now, tmrw_day_temp, tmrw_day_type, tmrw_night_temp, tmrw_night_type

        str_format = self.config[Cmd.TXT_EXECUTED]

        msg = str_format.format("Vilniuje", *getData("Vilnius")) + "\n\n"
        msg += str_format.format("Kaune", *getData("Kaunas")) + "\n\n"
        msg += str_format.format("Panevėžyje", *getData("Panevezys"))

        self.sendMessage(msg)


def getObj():
    return WeatherCmd()
