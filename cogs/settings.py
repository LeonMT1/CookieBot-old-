import asyncio

import discord
import discord.commands
from discord import slash_command, Option
from discord.ext import commands

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(0.7)
        print("""
            funcommands.py   ✅""")

    @slash_command(description="Personalisiere deine Einstellungen für den Bot")
    async def settings(self, ctx, einstellung: Option(str, description="Welche einstellung Möchtest du ändern?",
                                                      choices=["DM Narichten 🔔"]),
                       switch: Option(str, description="Soll die einstellung an oder aus sein?",
                                      choices=["an", "aus"])):
        guild: discord.Guild = self.bot.get_guild(724602228505313311)
        muterolle: discord.Role = guild.get_role(1043532505887809577)
        print(f"{ctx.author} hat die Einstellung {einstellung} auf {switch} gesetzt")
        if einstellung == "DM Narichten 🔔":
            if switch == "an":
                if muterolle not in ctx.author.roles:
                    await ctx.respond("Du hast die DM Narichten schon an!", ephemeral=True)
                    return
                await ctx.author.remove_roles(muterolle)
                await ctx.respond("Du hast die DM Narichten wieder angeschaltet.", ephemeral=True)
            elif switch == "aus":
                if muterolle in ctx.author.roles:
                    await ctx.respond("Du hast die DM Narichten schon aus!", ephemeral=True)
                    return
                await ctx.author.add_roles(muterolle)
                await ctx.respond("Du hast die DM Narichten ausgeschaltet.", ephemeral=True)


def setup(bot):
    bot.add_cog(Settings(bot))
