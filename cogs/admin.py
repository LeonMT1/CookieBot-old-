import asyncio
import json
import os
import random
import time
from datetime import datetime

import aiosqlite
import discord
import humanfriendly
from utils import *
import pytz
import requests
from discord import Option, slash_command
from discord.ext import commands, tasks
from discord.ui import Button, View
from dotenv import load_dotenv


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(0.3)
        print("""
            admin.py         ✅""")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == 1040793076744061009:
            if payload.emoji.name == "✅":
                print("LEL")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == 1040793076744061009:
            if payload.emoji.name == "❌":
                print("LEL2")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == 1040793076744061009:
            if payload.emoji.name == "🗑️":
                print("LEL3")

   # @slash_command(description="Reporte einen Bug")
   # async def bugreport(self, ctx, bugtitle: Option(str, description="Gebe deinen Bug einen Titel"),
   #                     bugdesc: Option(str, description="Beschreibe hier deinen Bug")):
   #     embed = discord.Embed(title=f"Bug Report von {ctx.author.name} | Title: {bugtitle}", description=f"""
#Beschreibung: {bugdesc}""")
     #   await self.bot.get_channel(1016436921750270034).send(embed=embed)


    @slash_command(description="Reporte einen Bug")
    async def reportbug(self, ctx):
        modal = embedModal(title="Mache ein Embed")
        await ctx.send_modal(modal)

def setup(bot):
    bot.add_cog(Admin(bot))

class embedModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label="Bug Titel",
                placeholder="zB: /event fehler!"),
            discord.ui.InputText(
                label="Bug Beschreibung",
                placeholder="zB: Wenn ich /event mache steht da ein Fehler!",
                style=discord.InputTextStyle.long),
            *args,
            **kwargs)

    async def callback(self, interaction: discord.Interaction):
        de = pytz.timezone('Europe/Berlin')
        member = interaction.user.name
        embed = discord.Embed(
            title=f"Bug Report von {member} | Titel: **{self.children[0].value}**",
            description=self.children[1].value,
            color=discord.Color.red(),
            timestamp=datetime.now().astimezone(tz=de))
        interaction = await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        dictionary = {message: message.id}

        with open("bug.json", "w") as outfile:
            json.dump(dictionary, outfile)

    async def on_raw_reaction_add(self, payload):
        with open("bug.json", "r") as f:
            json.object = json.loads(f.read())
        message = (json_object["message"])
        if payload.channel_id == 963728113920008212:
            if payload.message_id == message.id:
                if payload.emoji.name == "✅":
                     print("LEL")
