import asyncio
import random
import aiosqlite

import discord
import requests
from discord import slash_command, Option
from discord.ext import commands
import discord.commands


class Mathe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(0.6)
        print("""
            mathe.py         ✅""")

    @slash_command(description="Mache deine Mathe Aufgaben!")
    async def mathe(self, ctx, rechenart: Option(str, description="Wähle deine Rechenart aus", default=None,
                                                 choices=["+", "-", "*(mal)", "/(geteilt)"])):
        async with aiosqlite.connect("level.db") as db:
            async with db.execute("SELECT xp FROM users WHERE user_id = ?", (ctx.author.name,)) as cursor:
                mathe_xp = 2#= await cursor.fetchone()
            print(f"{ctx.author} hat /mathe gemacht.")
            mathe1 = random.randint(1, 10)
            mathe2 = random.randint(1, 100)
            mathe3 = random.randint(1, 1000)
            mathe4 = random.randint(1, 10000)
            rechenarten = ["+", "-", "*", "/"]
            if rechenart is None:
                rechenart = random.choice(rechenarten)
            if mathe_xp > 1000:
                if rechenart == "+":
                    await ctx.respond(f"{mathe2} {rechenart} {mathe2}")
                    ergebniss = mathe2 + mathe2
                    answer = self.bot.wait_for("message")
                    if answer == ergebniss:
                        embed = discord.Embed(title="Richtig!",
                                              description=f"Du liegst Richtig **{mathe2} {rechenart} {mathe2} ="
                                                          f" {ergebniss}.", color=discord.Color.green())
                        await ctx.respond(embed=embed)
                        return
                    embedflase = discord.Embed(title="Falsch!",
                                               description=f"Das ist Falsch! **{mathe2} {rechenart} {mathe2} = "
                                                           f"{ergebniss}.", color=discord.Color.red())
                    await ctx.respond(embed=embedflase)
                if rechenart == "-":
                    await ctx.respond(f"{mathe2} {rechenart} {mathe2}")
                    ergebniss = mathe2 - mathe2
                if rechenart == "*":
                    await ctx.respond(f"{mathe1} {rechenart} {mathe1}")
                    ergebniss = mathe1 * mathe1
                if rechenart == "/":
                    await ctx.respond(f"{mathe2} {rechenart} {mathe1}")
                    ergebniss = mathe2 / mathe1
            return


def setup(bot):
    bot.add_cog(Mathe(bot))
