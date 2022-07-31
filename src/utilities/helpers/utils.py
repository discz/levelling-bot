import discord


async def SendEmbed(title, colour, description=None):
    if not description:
        embed = discord.Embed(title=title, colour=colour)
    else:
        embed = discord.Embed(title=title, description=description, colour=colour)
    return embed

