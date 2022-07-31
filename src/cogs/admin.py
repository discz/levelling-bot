from discord.ext import commands
from src.utilities.helpers.utils import *


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load(self, ctx, cog: str):
        cog = f'cogs.{cog}'
        try:
            await self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(
                embed=await SendEmbed('Error:', discord.Colour.red(), f'{type(e).__name__} - {e}'))
        else:
            await ctx.channel.send(embed=await SendEmbed('✅ | Success!', discord.Colour.green()))

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, cog: str):
        cog = f'cogs.{cog}'
        try:
            await self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(
                embed=await SendEmbed('Error:', discord.Colour.red(), f'{type(e).__name__} - {e}'))
        else:
            await ctx.channel.send(embed=await SendEmbed('✅ | Success!', discord.Colour.green()))

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        cog = f'cogs.{cog}'
        try:
            await self.bot.reload_extension(cog)
        except Exception as e:
            await ctx.send(
                embed=await SendEmbed('Error:', discord.Colour.red(), f'{type(e).__name__} - {e}'))
        else:
            await ctx.channel.send(embed=await SendEmbed('✅ | Success!', discord.Colour.green()))


async def setup(bot):
    await bot.add_cog(AdminCog(bot))
