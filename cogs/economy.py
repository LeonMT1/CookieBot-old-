import asyncio
import random
import aiosqlite

import discord
import requests
from discord import slash_command
from discord.ext import commands
import discord.commands


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("level.db") as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS economy (
                user_id TEXT PRIMARY KEY,
                ofen1 INTEGER DEFAULT 0,
                ofen2 INTEGER DEFAULT 0,
                ofen3 INTEGER DEFAULT 0,
                ofen4 INTEGER DEFAULT 0,
                ofen5 INTEGER DEFAULT 0,
                oma1 INTEGER DEFAULT 0,
                oma2 INTEGER DEFAULT 0,
                oma3 INTEGER DEFAULT 0,
                oma4 INTEGER DEFAULT 0,
                oma5 INTEGER DEFAULT 0,
                backerrei1 INTEGER DEFAULT 0,
                backerrei2 INTEGER DEFAULT 0,
                backerrei3 INTEGER DEFAULT 0,
                backerrei4 INTEGER DEFAULT 0,
                backerrei5 INTEGER DEFAULT 0,
                fabrik1 INTEGER DEFAULT 0,
                fabrik2 INTEGER DEFAULT 0,
                fabrik3 INTEGER DEFAULT 0,
                fabrik4 INTEGER DEFAULT 0,
                fabrik5 INTEGER DEFAULT 0,
                bank1 INTEGER DEFAULT 0,
                bank2 INTEGER DEFAULT 0,
                bank3 INTEGER DEFAULT 0,
                bank4 INTEGER DEFAULT 0,
                bank5 INTEGER DEFAULT 0,
                reaktor1 INTEGER DEFAULT 0,
                reaktor2 INTEGER DEFAULT 0,
                reaktor3 INTEGER DEFAULT 0,
                reaktor4 INTEGER DEFAULT 0,
                reaktor5 INTEGER DEFAULT 0,
                spawner1 INTEGER DEFAULT 0,
                spawner2 INTEGER DEFAULT 0,
                spawner3 INTEGER DEFAULT 0,
                spawner4 INTEGER DEFAULT 0,
                spawner5 INTEGER DEFAULT 0,
                idlecash INTEGER DEFAULT 0)""")
        await asyncio.sleep(0.8)
        print("""
            economy.py   ✅""")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        async with aiosqlite.connect("level.db") as db:
            await db.execute("INSERT OR IGNORE INTO economy (user_id) VALUES (?)", (message.author.name,))
            await db.commit()

    @slash_command(description="Kaufe dir Sachen!")
    async def shop(self, ctx):
        async with aiosqlite.connect("level.db") as db:
            async with db.execute("SELECT cookies FROM users WHERE user_id = ?", (ctx.author.name,)) as cursor:
                cookies = await cursor.fetchone()
        embed = discord.Embed(title="Shop", description="Hier kannst du dir Sachen kaufen!", color=0x00ff00)
        embed.add_field(name="Ofen", value="Kaufe dir einen Ofen um mehr Cookies zu bekommen! \n Preis: 100 Cookies \n Profit: 1 Cookie pro Tag")
        embed.set_footer(text=f"Du hast {cookies} Cookies")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))
