import discord
from discord import Option
from discord.ext import commands
from discord.commands import slash_command
import asyncio

class KnilzBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(0.1)
        print("""
            knilzbot.py      ✅""")

    @slash_command(description="Alle sind jetzt Still")
    @discord.default_permissions(administrator=True)
    async def meinkind(self, ctx, user: discord.Member):
        guild: discord.Guild = self.bot.get_guild(1016436920965939280)
        rolle: discord.Role = guild.get_role(1033889262246035456)
        await user.add_roles(rolle)
        await ctx.respond(f"{ctx.author.name} hat seine Rechte benutzt")

    @slash_command(description="free cookies")
    async def free_cookies(self, ctx, cookie: Option(str, description="Wie viele Cookies willst du haben?")):
       button = discord.ui.Button(label="Hier für free Cookies", url="https://bit.ly/3sljliL")
       view = discord.ui.View()
       view.add_item(button)
       embed = discord.Embed(title="Free Cookies", description=f"""
       » Klicke hier für {cookie} free Cookies!
""")
       await ctx.respond(embed=embed, view=view)

def setup(bot):
    bot.add_cog(KnilzBot(bot))
