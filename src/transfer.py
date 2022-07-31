from databases import Database
import os
import json
import discord
from discord.ext import commands
from PIL import Image
import requests
from io import BytesIO

with open('users.json', 'r') as f:
    userssss = json.load(f)

db = Database('postgresql://postgres:root@localhost:5432/rework')
bot = commands.Bot(intents=discord.Intents.all(), command_prefix='!')


@bot.command(name='transfer')
async def transfer(ctx):
    print('working')
    await db.connect()
    count = 0
    guild = bot.get_guild(873258019180404736)
    for user in guild.members:
        if user:
            if user.bot:
                continue
            count += 1
            print(f'Adding #{count} - {user.name} to database')
            if user.avatar:
                avatar = user.avatar.with_format('png')
                avatar = requests.get(str(avatar)).content
            else:
                avatar = 'https://cdn.discordapp.com/embed/avatars/0.png'
                avatar = requests.get(str(avatar)).content

            if user.premium_since:
                premium = True
            else:
                premium = False
            send_data = "INSERT INTO userdata (userid, joined, lastname, pfp, premium, discriminator) " \
                        "VALUES (:userid, :joined, :lastname, :pfp, :premium, :discriminator)"
            values = {"userid": user.id, "joined": True, "lastname": user.name, "pfp": avatar,
                      "premium": premium, "discriminator": user.discriminator}
            update_data2 = "INSERT INTO levelling (userid, experience, level) VALUES (:userid, :exp, :level)"
            values2 = {"userid": user.id, "exp": 0, "level": 1}
            await db.execute(query=send_data, values=values)
            await db.execute(query=update_data2, values=values2)
            if count % 10 == 0:
                await ctx.send(f'{count} users added')
        else:
            pass
    await ctx.send(f'{count} users transferred to database!')
    await db.disconnect()


@bot.command(name='show')
async def show_pfp(ctx, user: discord.Member):
    await db.connect()
    user = await db.fetch_one("SELECT * FROM userdata WHERE userid = :userid", values={"userid": user.id})
    await db.disconnect()
    if user['pfp']:
        with BytesIO() as image_binary:
            stream = BytesIO(user['pfp'])
            image = Image.open(stream).convert("RGBA")
            image.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename='pfp.png'))



@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')


bot.run('ODk4NjgwNDk2NzMxNjExMTg3.YWnvbw.p7Kty7Cj9ucPxImrCBZxJ-Gw8TU')
