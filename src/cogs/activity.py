from discord.ext import commands
import discord
from databases import Database
from src.utilities.helpers.utils import SendEmbed
from src.utilities.helpers.dbops import DbOps
from src.utilities.levelling.calculations import Calculations
from requests import get
from random import randint

dbops = DbOps()
calc = Calculations()


class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        await dbops.add_user(member)
        await dbops.add_levelling(member)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return
        bucket = self.cd_mapping.get_bucket(ctx)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return
        user = await dbops.get_user(ctx.author)
        if user is None:
            await dbops.add_user(ctx.author)
        xp = await dbops.get_xp(ctx.author)
        premium = await dbops.get_premium(ctx.author)
        if not premium:
            xp += randint(15, 26)
        else:
            xp += randint(20, 35)
        await dbops.change_exp(ctx.author, xp)

        # Check if user has leveled up
        print(xp)
        curr_level = await calc.calculate_level(ctx.author, xp)
        print(curr_level)
        old_level = await dbops.get_level(ctx.author)
        print(old_level)
        if old_level < curr_level:
            await dbops.change_level(ctx.author, curr_level)

            await ctx.channel.send(embed=await SendEmbed("Level up!", discord.Color.green(),
                                                         f"{ctx.author.mention} has leveled up to level {curr_level}!"),
                                   delete_after=5)
        print('----------------------------------------------------')
        print(await 
              calc.calculate_level_xp(ctx.author, curr_level))


async def setup(bot):
    await bot.add_cog(Activity(bot))
