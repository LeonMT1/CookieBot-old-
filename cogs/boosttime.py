import discord
import asyncio
from discord.commands import Option
from discord.ext import commands
from discord.commands import slash_command, SlashCommandGroup
from discord.utils import format_dt


class Boostime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(1.2)
        print("""
            boosttime.py     ✅""")

    @slash_command(name="nitrozeit", description="Zeigt dir an wie lange leute den Server Boosten!")
    async def boostime(self, ctx, member: Option(discord.Member, "Wähle ein Server-Mitglied aus!", required=False)):
        user = member or ctx.author
        boostzeit = user.premium_since

        if user.bot:
            await ctx.respond(content="**`❌` | Bots können denn Server nicht boosten!**")
            return
        if user not in ctx.guild.members:
            await ctx.respond(content="**`❌` | Dieser User ist nicht auf diesem Server!**")
            return

        if boostzeit is None:
            await ctx.respond(content="**`❌` | Dieser User hat noch nicht geboostet!**")
            return

        else:
            boostzeit = ctx.author.premium_since
            boostzeit = format_dt(boostzeit, style="R")
            await ctx.respond(content=f"**`🚀` | Du hast das Server Boosting auf diesem Server {boostzeit} gestartet!**")


def setup(bot):
    bot.add_cog(Boostime(bot))
