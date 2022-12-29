import discord
from discord.ext import commands
from discord.commands import slash_command, option
import aiohttp
import asyncio

class mcstats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(0.9)
        print("""
            mcstats.py       ✅""")

    @slash_command()
    @option(name="auswahl", description="Wähle eine Option", required=True, choices=["Java", "Bedrock"])
    async def minecraftstats(self, ctx, auswahl, ip):
        try:
            if auswahl == "Bedrock":
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://api.mcsrvstat.us/bedrock/2/{ip}") as r:
                        res = await r.json()
                        if res['online'] == True:
                            embed = discord.Embed(
                                title="Minecraft Server Stats",
                                description=f"IP: {ip} | Port: {res['port']}",
                                color=discord.Color.green()
                            )
                            embed.add_field(name="Online", value='Ja')
                            embed.add_field(name="Version", value=res['version'])
                            embed.add_field(name="Players", value=res['players']['online'])
                            embed.add_field(name="Max Players", value=res['players']['max'])
                            embed.add_field(name="Software", value=res['software'])
                            await ctx.respond(embed=embed)
                        else:
                            embed = discord.Embed(
                                title="Fehler",
                                description="Der Server ist Offline",
                                color=discord.Color.embed_background()
                            )
                            await ctx.respond(embed=embed)
            elif auswahl == "Java":
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://api.mcsrvstat.us/2/{ip}") as r:
                        res = await r.json()
                        if res['online'] == True:
                            embed = discord.Embed(
                                title="Minecraft Server Stats",
                                description=f"IP: {ip} | Port: {res['port']}",
                                color=discord.Color.green()
                            )
                            embed.add_field(name="Online", value='Ja')
                            embed.add_field(name="Version", value=res['version'])
                            embed.add_field(name="Players", value=res['players']['online'])
                            embed.add_field(name="Max Players", value=res['players']['max'])
                            embed.add_field(name="Software", value=res['software'])
                            await ctx.respond(embed=embed)
                        else:
                            embed = discord.Embed(
                                title="Fehler",
                                description="Der Server ist Offline",
                                color=discord.Color.embed_background()
                            )
                            await ctx.respond(embed=embed)
        except:
            await ctx.respond("Server nicht gefunden", ephemeral=True)


def setup(bot):
    bot.add_cog(mcstats(bot))