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

    @slash_command()
    async def bug_report(self, ctx):
        await ctx.respond("Wir haben dein Bug erhalten und werden ihn so schnell wie möglich beheben. "
                          "Vielen Dank für deine Mithilfe!")

def setup(bot):
    bot.add_cog(Admin(bot))

class TutorialModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label="Bug Titel",
                placeholder="z.B Bug bei /events"),
            discord.ui.InputText(
                label="Bug Beschreibung",
                placeholder="z.B wenn ich /events eingebe, dann passiert nichts",
                style=discord.InputTextStyle.long),
            *args,
            **kwargs)

    async def callback(self, interaction):
        guild: discord.Guild = self.bot.get_guild(1016436920965939280)
        rolle: discord.channel = guild.get_role(1033889262246035456)
        embed = discord.Embed(
            title=self.children[0].value,
            description=self.children[1].value,
            color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
