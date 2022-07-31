from databases import Database
from requests import get
import discord
from io import BytesIO
from PIL import Image
from requests import get
from asyncpg import exceptions


class DbOps:
    def __init__(self):
        self.db = Database('postgresql://postgres:root@localhost:5432/dc_rework')

    # Add queries

    async def add_user(self, member: discord.Member):
        await self.db.connect()
        if member:
            if member.avatar:
                avatar = member.avatar.with_format('png')
                avatar = get(str(avatar)).content
            else:
                avatar = 'https://cdn.discordapp.com/embed/avatars/0.png'
                avatar = get(str(avatar)).content
                print(type(avatar))

            if member.premium_since:
                premium = True
            else:
                premium = False
            send_data = "INSERT INTO userdata (userid, joined, lastname, pfp, premium, discriminator) " \
                        "VALUES (:userid, :joined, :lastname, :pfp, :premium, :discriminator)"
            values = {"userid": member.id, "joined": True, "lastname": member.name, "pfp": avatar,
                      "premium": premium, "discriminator": member.discriminator}
            send_data2 = "INSERT INTO levelling (userid, experience, level) VALUES (:userid, :exp, :level)"
            values2 = {"userid": member.id, "exp": 0, "level": 1}
            try:
                await self.db.execute(query=send_data, values=values)
                await self.db.execute(query=send_data2, values=values2)
            except exceptions.UniqueViolationError:
                pass
            await self.db.disconnect()

    # Update User queries

    async def change_lastname(self, member: discord.Member, lastname):
        await self.db.connect()
        update_data = "UPDATE userdata SET lastname = :? WHERE userid = :?"
        values = {"userid": member.id, "lastname": lastname}
        await self.db.execute(query=update_data, values=values)
        await self.db.disconnect()

    async def change_pfp(self, member: discord.Member):
        await self.db.connect()
        if member.avatar:
            avatar = member.avatar.with_format('png')
            avatar = get(str(avatar)).content
        else:
            avatar = 'https://cdn.discordapp.com/embed/avatars/0.png'
            avatar = get(str(avatar)).content
        update_data = "UPDATE userdata SET pfp = :pfp WHERE userid = :userid"
        values = {"userid": member, "pfp": avatar}
        await self.db.execute(query=update_data, values=values)
        await self.db.disconnect()

    async def change_premium(self, member: discord.Member):
        await self.db.connect()

        if member.premium_since:
            premium = True
        else:
            premium = False

        update_data = "UPDATE userdata SET premium = :premium WHERE userid = :userid"
        values = {"userid": member.id, "premium": premium}
        await self.db.execute(query=update_data, values=values)
        await self.db.disconnect()

    async def change_joined(self, member: discord.Member, joined):
        await self.db.connect()
        update_data = "UPDATE userdata SET joined = :joined WHERE userid = :userid"
        values = {"userid": member.id, "joined": joined}
        await self.db.execute(query=update_data, values=values)
        await self.db.disconnect()

    async def change_discriminator(self, member: discord.Member):
        await self.db.connect()
        update_data = "UPDATE userdata SET discriminator = :discriminator WHERE userid = :userid"
        values = {"userid": member.id, "discriminator": member.discriminator}
        await self.db.execute(query=update_data, values=values)
        await self.db.disconnect()

    async def change_exp(self, member: discord.Member, exp):
        await self.db.connect()
        update_data = "UPDATE levelling SET experience = :exp WHERE userid = :userid"
        values = {"userid": member.id, "exp": exp}
        await self.db.execute(query=update_data, values=values)
        await self.db.disconnect()

    async def change_level(self, member: discord.Member, level):
        await self.db.connect()
        update_data = "UPDATE levelling SET level = :level WHERE userid = :userid"
        values = {"userid": member.id, "level": level}
        await self.db.execute(query=update_data, values=values)
        await self.db.disconnect()

    # Get User queries

    async def get_user(self, member: discord.Member):
        await self.db.connect()
        get_data = "SELECT * FROM userdata WHERE userid = :userid"
        values = {"userid": member.id}
        result = await self.db.fetch_one(query=get_data, values=values)
        await self.db.disconnect()
        return result

    async def get_lastname(self, member: discord.Member):
        await self.db.connect()
        get_data = "SELECT lastname FROM userdata WHERE userid = :userid"
        values = {"userid": member.id}
        result = await self.db.fetch_one(query=get_data, values=values)
        await self.db.disconnect()
        return result['lastname']

    async def get_pfp(self, member: discord.Member):
        await self.db.connect()
        get_data = "SELECT pfp FROM userdata WHERE userid = :userid"
        values = {"userid": member.id}
        result = await self.db.fetch_one(query=get_data, values=values)
        if result['pfp']:
            with BytesIO() as image_binary:
                stream = BytesIO(result['pfp'])
                image = Image.open(stream).convert("RGBA")
                image.save(image_binary, 'PNG')
                image_binary.seek(0)
                await self.db.disconnect()
                return image_binary

    async def get_premium(self, member: discord.Member):
        await self.db.connect()
        get_data = "SELECT premium FROM userdata WHERE userid = :userid"
        values = {"userid": member.id}
        result = await self.db.fetch_one(query=get_data, values=values)
        await self.db.disconnect()
        return result['premium']

    async def get_joined(self, member: discord.Member):
        await self.db.connect()
        get_data = "SELECT joined FROM userdata WHERE userid = :userid"
        values = {"userid": member.id}
        result = await self.db.fetch_one(query=get_data, values=values)
        await self.db.disconnect()
        return result['joined']

    # Get levelling data

    async def get_xp(self, member: discord.Member):
        await self.db.connect()
        get_data = "SELECT experience FROM levelling WHERE userid = :userid"
        values = {"userid": member.id}
        result = await self.db.fetch_one(query=get_data, values=values)
        await self.db.disconnect()
        return result['experience']

    async def get_level(self, member: discord.Member):
        await self.db.connect()
        get_data = "SELECT level FROM levelling WHERE userid = :userid"
        values = {"userid": member.id}
        result = await self.db.fetch_one(query=get_data, values=values)
        await self.db.disconnect()
        return result['level']

    async def get_rank(self, member: discord.Member):
        await self.db.connect()
        get_data = "SELECT rank FROM levelling WHERE userid = :userid"
        values = {"userid": member.id}
        result = await self.db.fetch_one(query=get_data, values=values)
        await self.db.disconnect()
        return result['rank']
