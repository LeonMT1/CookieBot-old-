import asyncio
import aiosqlite

import discord
import requests
from discord import Option
from discord.ext import commands
from discord.commands import slash_command


class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("afk.db") as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS afk (
                user_id TEXT PRIMARY KEY,
                afk INTEGER DEFAULT 0,
                grund TEXT DEFAULT hat keinen Grund angegeben)""")
        await asyncio.sleep(0.5)
        print("""
            afk.py           ✅""")
# 0 heißt nicht afk 1 heißt afk

    @slash_command(description="Stelle deinen Status auf AFK")
    async def afk(self, ctx, grund: Option(str, description="Warum bist du AFK?", default=None)):
        async with aiosqlite.connect("afk.db") as db:
            await db.execute("INSERT OR IGNORE INTO afk (user_id) VALUES (?)", (ctx.author.name,))
            await db.commit()
            if grund is None:
                grund = "Du hast keinen Grund angegeben"
            await ctx.respond(f"Du hast deinen Status erfolgreich auf AFK geändert! Grund: **{grund}**.",
                              ephemeral=True)
            if grund == "Du hast keinen Grund angegeben":
                grund = f"{ctx.author.name} hat keinen Grund angegeben"
            await db.execute("UPDATE grund SET ? WHERE user_id = ?", (grund, ctx.author.name))
            await db.execute("UPDATE afk SET 1 WHERE user_id = ?", (ctx.author.name,))
            await db.commit()

def setup(bot):
    bot.add_cog(AFK(bot))
