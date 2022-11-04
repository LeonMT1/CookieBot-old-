import asyncio
import random
import aiosqlite

import discord
from discord import Option
import requests
from discord.ext import commands
from discord.commands import slash_command


class MMOSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("mmo.db") as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS mmostats (
                user_id TEXT PRIMARY KEY,
                username TEXT DEFAULT nope,
                profilurl TEXT DEFAULT nope
                klasse TEXT DEFAULT nope,
                leben INTEGER DEFAULT 0,
                defens INTEGER DEFAULT 0
                mana INTEGER DEFAULT 0,
                stamina INTEGER DEFAULT 0,
                stärke INTEGER DEFAULT 0,
                level INTEGER DEFAULT 0)""")
        await asyncio.sleep(0.4)
        print("""
            mmosystem.py     ✅""")

    @slash_command(description="Erstelle deinen Charakter")
    async def mmo_create(self, ctx, url: Option(str,
                                                description="Füge eine URL von einen gewünschten Bild als Avatar ein",
                                                default=None),
                         name: Option(str, description="Schreibe deinen gewünschten MMO Namen", default=None),
                         klasse: Option(str, choises=["Cookie Krieger", "Zauberer", "Tank", "Gigachad", "Usain Bolt"])):
        async with aiosqlite.connect(self.DB) as db:
            if name is None:
                name = ctx.author.name
            if url is None:
                url = ctx.author.display_avatar.url
            await db.execute("INSERT OR IGNORE INTO mmostats (user_id) VALUES (?)", (ctx.author.name,))
            await db.execute("UPDATE mmostats SET username ? WHERE user_id = ?", (name, ctx.author.name))
            await db.execute("UPDATE mmostats SET profilurl ? WHERE user_id = ?", (url, ctx.author.name))
            await db.execute("UPDATE mmostats SET klasse ? WHERE user_id = ?", (klasse, ctx.author.name))
            await db.commit()


def setup(bot):
    bot.add_cog(MMOSystem(bot))