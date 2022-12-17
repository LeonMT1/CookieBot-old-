import asyncio
import random
import aiosqlite

import discord
import requests
from discord import slash_command
from discord.ext import commands
import discord.commands


class BugReport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(0.3)
        print("""
            funcommands.py   ✅""")



def setup(bot):
    bot.add_cog(BugReport(bot))