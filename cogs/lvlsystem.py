import asyncio
import random

import aiosqlite
import discord
from discord import Option
from discord.commands import slash_command
from discord.ext import commands


class LVLSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = "level.db"

    @staticmethod
    def get_level(xp):
        lvl = 1
        amount = 100

        while True:
            xp -= amount
            if xp < 0:
                return lvl
            lvl += 1
            amount += 75

    @staticmethod
    async def xp_to_next_level(xp):
        lvl = LVLSystem.get_level(xp)
        return 175 + (75 * lvl)

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("level.db") as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                msg_count INTEGER DEFAULT 0,
                xp INTEGER DEFAULT 0,
                cookies INTEGER DEFAULT 0,
                call_sec INTEGER DEFAULT 0,
                mathe_xp INTEGER DEFAULT 0,
                mathe_geschaft INTEGER DEFAULT 0)""")
            print("""
            ---Datein------Status---
            main.py          ✅
            lvlsystem.py     ✅""")

    async def check_user(self, user_id):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
            await db.commit()

    async def get_xp(self, user_id):
        await self.check_user(user_id)
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()
            return result[0]

    @commands.Cog.listener()
    async def on_message(self, message):
        async with aiosqlite.connect("level.db") as db:
            channels = [992840704734797834, 992840882397130832, 992840853687111721, 992840783621271582]
            if message.author.bot:
                return
            if not message.guild:
                return
            guild: discord.Guild = self.bot.get_guild(724602228505313311)
            rolle: discord.Role = guild.get_role(1055216204878446754)
            xp = random.randint(15, 25)
            if rolle in message.author.roles:
                xp = xp * 1.5
            if message.channel.id in channels:
                xp = xp / 2
            rndm = random.randint(1, 100)
            await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (message.author.name,))
            await db.execute("UPDATE users SET msg_count = msg_count + 1, xp = xp + ? WHERE user_id = ?",
                             (xp, message.author.name))
            await db.commit()
            print(xp)
            glueckembed = discord.Embed(title="Kleine Belohnung;)",
                                        description=f"{message.author.name} hat {xp} Cookies bekommen da er aktiv am "
                                                    f"Chat teilgenommen has!", color=discord.Color.green())

            if rndm == 1:
                await message.channel.send(embed=glueckembed)
                await db.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", (xp, message.author.name))
                await db.commit()

        new_xp = await self.get_xp(message.author.name)
        old_level = self.get_level(new_xp - xp)
        new_level = self.get_level(new_xp)
        lvlcookies = new_level * 5

        embed = discord.Embed(title="Rangaufstieg", color=discord.Color.random(),
                              description=f"Herzlichen Glückwunsch {message.author.mention} du hast Level **{new_level}"
                                          f"** ereicht! Du hast **{lvlcookies}** Cookies als Geschenk bekommen!")

        if old_level == new_level:
            return
        async with aiosqlite.connect("level.db") as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?",
                                     (lvlcookies, message.author.name))
                await db.commit()
            await message.channel.send(embed=embed)

    @slash_command()
    async def rank(self, ctx, user: Option(discord.Member, description="Von welchen User möchtest du den Rank wissen?",
                                           default=None)):
        async with aiosqlite.connect(self.DB) as db:
            if user is None:
                user = ctx.author

            async with db.execute("SELECT cookies FROM users WHERE user_id = ?", (user.name,)) \
                    as cursor:
                cookies = await cursor.fetchone()

            async with db.execute("SELECT msg_count FROM users WHERE user_id = ?", (user.name,)) \
                    as cursor:
                msg_count = await cursor.fetchone()

            async with db.execute("SELECT call_sec FROM users WHERE user_id = ?", (user.name,)) \
                    as cursor:
                call_sec = await cursor.fetchone()

        # async with db.execute("SELECT mathe_xp FROM users WHERE user_id = ?", (user.name,)) as cursor:
        #    mathe_xp = await cursor.fetchone()

        xp = await self.get_xp(user.name)
        lvl = self.get_level(xp)
        xp_to_next_level = await self.xp_to_next_level(xp)

        # mathe_lvl = self.get_level(mathe_xp)

        embed = discord.Embed(title=f"{user.name} Rank", color=discord.Color.random())
        embed.add_field(name="XP", value=f"{user.name} hat **{xp}/{xp_to_next_level}** XP und ist daher Level **{lvl}**"
                                         f".", inline=True)
        embed.add_field(name="Talk Zeit", value=f"{user.name} war **{call_sec[0]}** Sekunden in Talks.", inline=True)
        embed.add_field(name="Cookies", value=f"{user.name} hat **{cookies[0]}** Cookies.", inline=True)
        embed.add_field(name="Narichten", value=f"{user.name} hat **{msg_count[0]}** Narichten geschrieben.",
                        inline=True)
        #        embed.add_field(name="Mathe", value=f"""
        # Mathe XP: {mathe_xp}
        # Mathe LVL: {mathe_lvl}""")
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=f"Angefordert von {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.respond(embed=embed)

    @slash_command()
    async def leaderboard(self, ctx, leaderboard: Option(str, choices=["Cookies", "Narichten", "XP", "Talk",
                                                                       "Mathe (sneak peak)"],
                                                         description="Wähle eine Leaderboard aus"),
                          member: Option(str, description="Sage wie viele Member angezeigt werden sollen", default=10)):
        desc = ""
        counter = 1
        async with aiosqlite.connect("level.db") as db:

            if leaderboard == "Cookies":
                async with db.execute(
                        "SELECT user_id, cookies FROM users WHERE cookies > 0 ORDER BY cookies DESC LIMIT ?",
                        (member,)) as cursor:
                    async for user_id, cookies in cursor:
                        desc += f"{counter}. **{user_id}** - **{cookies}** {leaderboard}\n"
                        counter += 1

                embed = discord.Embed(title=f"**{leaderboard} Rangliste**", description=desc,
                                      color=discord.Color.orange())
                await ctx.respond(embed=embed)
                return

            if leaderboard == "Narichten":
                async with db.execute(
                        "SELECT user_id, msg_count FROM users WHERE msg_count > 0 ORDER BY msg_count DESC LIMIT ?",
                        (member,)) as cursor:
                    async for user_id, msg_count in cursor:
                        desc += f"{counter}. **{user_id}** - **{msg_count}** {leaderboard}\n"
                        counter += 1

                embed = discord.Embed(title=f"**{leaderboard} Rangliste**", description=desc,
                                      color=discord.Color.blue())
                await ctx.respond(embed=embed)
                return

            if leaderboard == "XP":
                async with db.execute("SELECT user_id, xp FROM users WHERE xp > 0 ORDER BY xp DESC LIMIT ?",
                                      (member,)) as cursor:
                    async for user_id, xp in cursor:
                        lvl = self.get_level(xp)
                        desc += f"{counter}. **{user_id}** - **{xp}** {leaderboard} - Level **{lvl}**\n"
                        counter += 1

                embed = discord.Embed(title=f"**{leaderboard} Rangliste**", description=desc,
                                      color=discord.Color.green())
                await ctx.respond(embed=embed)
                return

            # if leaderboard == "Mathe":
            #    async with db.execute("SELECT user_id, mathe_xp FROM users WHERE xp > 0 ORDER BY xp DESC LIMIT ?",
            #                         (member,)) as cursor:
            #      async for user_id, mathe_xp in cursor:
            #         desc += f"{counter}. **{user_id}** - **{mathe_xp}** {leaderboard}\n"
            #        counter += 1

            # embed = discord.Embed(title=f"**{leaderboard} Rangliste**", description=desc,
            #                       color=discord.Color.blue())
            # await ctx.respond(embed=embed)
            # return

            if leaderboard == "Talk":
                async with db.execute(
                        "SELECT user_id, call_sec FROM users WHERE call_sec > 0 ORDER BY call_sec DESC LIMIT ?",
                        (member,)) as cursor:
                    async for user_id, call_sec in cursor:
                        desc += f"{counter}. **{user_id}** - **{call_sec}** Sekunden {leaderboard}\n"
                        counter += 1

                embed = discord.Embed(title=f"**{leaderboard} Rangliste**", description=desc,
                                      color=discord.Color.dark_blue())
                await ctx.respond(embed=embed)

    @slash_command(description="Gebe einen anderen User Kekse!")
    async def gift(self, ctx, user: discord.Member, betrag: Option(int, description="Wie viel möchtest du geben?")):
        async with aiosqlite.connect("level.db") as db:
            async with db.execute("SELECT cookies FROM users WHERE user_id = ?", (ctx.author.name,)) as cursor:
                result = await cursor.fetchone()
                print(f"{ctx.author} hat /give gemacht")
                if user == ctx.author:
                    await ctx.respond("Du kannst dir nicht selber Kekse geben!", ephemeral=True)
                    return
                if user == user.bot:
                    await ctx.respond("Das ist zwar nett gemeint aber die Bots verdienen genung.", ephemeral=True)
                    return
                if result[0] < betrag:
                    await ctx.respond(f"Du hast nicht genug Cookies, du hast nur **{result[0]}** Cookies.",
                                      ephemeral=True)
                    return
            await db.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", (betrag, user.name))
            await db.execute("UPDATE users SET cookies = cookies - ? WHERE user_id = ?", (betrag, ctx.author.name))
            await db.commit()
            await ctx.respond(f"Du hast erfolgreich **{user.name}** **{betrag}** Cookies gegeben.", ephemeral=True)
            async with db.execute("SELECT cookies FROM users WHERE user_id = ?", (user.name,)) as cursor2:
                userresult = await cursor2.fetchone()
            await user.send(f"Du hast von {ctx.author.name} **{betrag}** Cookies bekommen. Du hast jetzt "
                            f"**{userresult[0]}** Cookies.")

    @slash_command(description="Esse einen Keks")
    async def eat(self, ctx, cookies: Option(int, description="Wie viele Kekse möchtest du essen?")):
        async with aiosqlite.connect("level.db") as db:
            async with db.execute("SELECT cookies FROM users WHERE user_id = ?", (ctx.author.name,)) as cursor:
                result = await cursor.fetchone()
            if result[0] < 1:
                await ctx.respond("Du hast keine Cookies.", ephemeral=True)
                return
            guild: discord.Guild = self.bot.get_guild(724602228505313311)
            rolle: discord.Role = guild.get_role(1055216204878446754)
            xpboost = cookies * 5
            await db.execute("UPDATE users SET cookies = cookies - ? WHERE user_id = ?", (cookies, ctx.author.name))
            await db.commit()
            if cookies == 1:
                embed = discord.Embed(title="Du hast einen Keks gegessen!",
                                      description=f"Du hast **{cookies}** Keks gegessen und einen x1.5 XP Boost für "
                                                  f"**{xpboost}** Minuten bekommen!",
                                      color=discord.Color.green())
                await ctx.respond(embed=embed)
                await ctx.author.add_roles(rolle)
                await asyncio.sleep(xpboost * 60)
                await ctx.author.remove_roles(rolle)
                await ctx.author.send(f"Dein XP Boost ist vorbei.")
                return
            embed = discord.Embed(title="Du hast Kekse gegessen!",
                                  description=f"Du hast **{cookies}** Kekse gegessen und einen x1.5 XP Boost für "
                                              f"**{xpboost}** Minuten bekommen!", color=discord.Color.green())
            await ctx.respond(embed=embed)
            await ctx.author.add_roles(rolle)
            await asyncio.sleep(xpboost * 60)
            await ctx.author.remove_roles(rolle)
            await ctx.author.send(f"Dein XP Boost ist vorbei.")


def setup(bot):
    bot.add_cog(LVLSystem(bot))
