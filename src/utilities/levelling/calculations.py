import math

from databases import Database
from src.utilities.helpers.dbops import DbOps
import discord
from math import log, floor

db = DbOps()


class Calculations:
    def __init__(self):
        pass

    @staticmethod
    async def calculate_level(member: discord.Member, xp: int):
        if xp < 5000:
            a = int(xp) / 100
            b = log(a, 1.55)
            lvl_end = math.floor(b) + 1
            return lvl_end

        else:
            a = xp / 1000
            lvl_end = a + 5
            lvl_end = math.floor(lvl_end)
            return lvl_end

    @staticmethod
    async def calculate_level_xp(member: discord.Member, level: int):
        print("level: " + str(level))
        if level < 10:
            if level == 9:
                start_exp = 100 * (1.55 ** (level - 1))
                end_exp = (level - 4) * 1000
                return start_exp, end_exp
            else:
                start_exp = 100 * (1.55 ** (level - 1))
                end_exp = 100 * (1.55 ** ((level + 1) - 1))
                end_exp = math.floor(end_exp)
                return start_exp, end_exp
        else:
            start_exp = (level - 5) * 1000
            end_exp = (level - 4) * 1000
            return start_exp, end_exp
