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
        embed = discord.Embed(
            title=f"Bug Report von **LÜCKE** | Titel: **{self.children[0].value}**",
            description=self.children[1].value,
            color=discord.Color.red(),
            timestamp=datetime.now().astimezone(tz=de))
        message = await interaction.response.send_message(embed=embed)
        messgaeid = message.id
        print(messgaeid)
        await messgaeid.add_reaction("✅")
        await messgaeid.add_reaction("❌")
