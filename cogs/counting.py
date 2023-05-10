import asyncio
import ast
import random
import aiosqlite
import time
import os
import json

import discord
import requests
from discord import slash_command
from discord.ext import commands
import discord.commands

class CountingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.count = 0
        self.previous_author = None
        self.data_file = "counting_data.json"  # name of the JSON file

        # create the JSON file if it doesn't exist
        if not os.path.isfile(self.data_file):
            with open(self.data_file, "w") as f:
                json.dump({"count": 0}, f)

        # read the last saved count from the JSON file and set it as the starting point
        with open(self.data_file, "r") as f:
            self.count = json.load(f)["count"]

    @commands.Cog.listener()
    async def on_ready(self):
        channel = 1073159625681162260
        await asyncio.sleep(1.0)
        print("""
            counting.py      ✅""")
        await self.bot.get_channel(1073159625681162260).send("**0**")
        
    @commands.Cog.listener()
    async def on_message(self, message):
        async with aiosqlite.connect("level.db") as db:
            if message.author.bot:
                return
            embed = discord.Embed(title="Verkackt!", description=f"{message.author.name} hat die Falsche Zahl geschrieben.", color=discord.Color.red())
            embed2 = discord.Embed(title="Verkackt!", description=f"{message.author.name} du kannst nicht alleine Zählen du Egoist.")
            if message.channel.id == 1073159625681162260:
                if message.content.isdigit():
                    if self.previous_author == message.author:
                        self.count = 0
                        await message.channel.send(embed=embed2)
                        await message.channel.send("**0**")
                    elif int(message.content) == self.count + 1:
                        self.count += 1
                        self.previous_author = message.author
                        await message.add_reaction('✅')
                        await db.execute("UPDATE users SET cookies = cookies + 1 WHERE user_id = ?", (message.author.name,))
                        await db.commit()
                    else:
                        self.count = 0
                        self.previous_author = None
                        await message.channel.send(embed=embed)
                        await message.channel.send("**0**")


def setup(bot):
    bot.add_cog(CountingCog(bot))
