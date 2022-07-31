import discord
from databases import Database
from discord.ext import commands
from discord.ext import tasks
from asyncio import run

initial_extensions = ['cogs.admin', 'cogs.activity']

database = Database('postgresql://postgres:root@localhost:5432/rework')
bot = commands.Bot(intents=discord.Intents.all(), command_prefix='!')


async def main():
    async with bot:
        for extension in initial_extensions:
            await bot.load_extension(extension)
        await bot.start('ODk4NjgwNDk2NzMxNjExMTg3.YWnvbw.p7Kty7Cj9ucPxImrCBZxJ-Gw8TU')

run(main())
print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')