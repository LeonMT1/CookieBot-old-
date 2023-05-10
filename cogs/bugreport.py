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
            bugreport.py     ✅""")

@commands.Cog.listener()
async def on_message(message):
    #bug channel id ersetzen
    if message.channel.id == 1071805141591793806:
        #mod chat channel ersetzten
        channel = bot.get_channel(1071805178312917105)
        embed = discord.Embed(title="**Neuer Bug:**", description=message.content, color=discord.Color.red())
        await channel.send(embed=embed, view=BugView(message.author))
        await message.delete()

class BugView(discord.ui.View):
    def __init__(self, user):
        self.user = user
        super().__init__(timeout=None)

@discord.ui.button(label="✅", style=discord.ButtonStyle.green)
async def button_callback1(self, button, interaction):
    async with aiosqlite.connect("level.db") as db:
        await interaction.response.send_message(f"Bug wurde bestätigt, der Member bekommt Cookies")
        # Hier soll der User Cookies bekommen
        member = self.user
        member2 = self.user.name
        cookies = random.randit(10, 50)
        await db.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", (cookies, member2))
        await db.commit()
        #role id ersetzen
        role = discord.utils.get(member.guild.roles, id=1043532505887809577)
        if role not in member.roles:
            await member.send("Du hast durch das reporten eines Bugs Cookies erhalten")
        else:
            return

@discord.ui.button(label="❌", style=discord.ButtonStyle.green)
async def button_callback2(self, button, interaction):
    await interaction.response.send_message(f"Bug wurde nicht bestätigt, der Member bekommt keine Cookies")
    role = discord.utils.get(member.guild.roles, id=1043532505887809577)
    if role not in member.roles:
        await member.send("Du hast einen Bug Reportet doch unsere Mods haben diesen für Unwichtig oder nicht exestierend eingestuft.")
    else:
        return

def setup(bot):
    bot.add_cog(BugReport(bot))
