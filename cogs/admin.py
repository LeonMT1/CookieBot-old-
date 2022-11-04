import asyncio
import datetime
import json

import discord
import pytz
import requests
from discord import Option
from discord.ext import commands
from discord.commands import slash_command


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(0.3)
        print("""
            admin.py         ✅""")

    @slash_command(description='Reporte einen Bug')
    async def bugreport(self, ctx, bug: Option(str, description="Reporte einen Bug")):
        print(f"{ctx.author.name} hat /bugreport gemacht")
        class MyModal(discord.ui.Modal):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(
                    discord.ui.InputText(
                            label="Bug Title",
                            placeholder="BSP. /event geht nicht",
                        ),
                        discord.ui.InputText(
                            label="Bug Beschreibung",
                            placeholder="BSP. /event geht ned wenn ich das mache steht da Anwendung Reagiert nicht",
                            style=discord.InputTextStyle.long,
                        ),
                        *args,
                        **kwargs,
                    )

                async def callback(self, interaction: discord.Interaction):
                    reportchannel = self.bot.get_channel(1016436921750270034)
                    de = pytz.timezone('Europe/Berlin')
                    title = value = self.children[0].value
                    desc = value = self.children[1].value
                    embed = discord.Embed(title=f"{title}", description=f"{desc}", color=discord.Color.random(),
                                          timestamp=datetime.now().astimezone(tz=de))
                    await self.bot.get_channel(reportchannel).send(embed=embed)
                    msg_id = msg.id
                    with open('rr.json', 'r') as f:
                        rr = json.load(f)
                    rr[str(msg_id)] = role.id
                    with open('rr.json', 'w') as f:
                        rr = json.dump(rr, f)
                        msg = bot.get_message(msg_id)
                        await msg.add_reaction("✅")
                        embed = discord.Embed(title="Erfolgreich erstellt!", color=discord.Color.green())
                        await interaction.response.send_message(embed=embed, ephemeral=True)

            modal = MyModal(title="Embed Builder")
            await ctx.send_modal(modal)

    @bot.event
    async def on_raw_reaction_add(payload):
        guild2 = bot.get_guild(payload.guild_id)
        member2: discord.Member = guild2.get_member(payload.user_id)
        if not member2.bot:
            with open('rr.json', 'r') as f:
                data = json.load(f)
            if str(payload.message_id) in data:
                member = payload.member
                guild = member.guild
                roleid = data[str(payload.message_id)]
                role = discord.utils.get(guild.roles, id=roleid)
                if role == None or not role.is_assignable:
                    _channel = discord.utils.get(guild.channels, id=payload.channel_id)
                    await _channel.send(
                        'Ich habe keine Rechte um diese Rolle anderen zu geben oder sie wurde gelöscht!')
                    return
                try:
                    await member.add_roles(role)
                except discord.Forbidden:
                    _channel = discord.utils.get(guild.channels, id=payload.channel_id)
                    await _channel.send(
                        'Ich habe keine Rechte um diese Rolle anderen zu geben oder sie wurde gelöscht!')

    @bot.event
    async def on_raw_reaction_remove(payload):
        guild2 = bot.get_guild(payload.guild_id)
        member2: discord.Member = guild2.get_member(payload.user_id)
        if not member2.bot:
            with open('rr.json', 'r') as f:
                data = json.load(f)
            if str(payload.message_id) in data:
                member2 = guild2.get_member(payload.user_id)
                guild = member2.guild
                roleid = data[str(payload.message_id)]
                role = discord.utils.get(guild.roles, id=roleid)
                if role == None or not role.is_assignable:
                    _channel = discord.utils.get(guild.channels, id=payload.channel_id)
                    await _channel.send(
                        'Ich habe keine Rechte um diese Rolle anderen zu geben oder sie wurde gelöscht!')
                try:
                    await member2.remove_roles(role)
                except discord.Forbidden:
                    _channel = discord.utils.get(guild.channels, id=payload.channel_id)
                    await _channel.send(
                        'Ich habe keine Rechte um diese Rolle anderen zu geben oder sie wurde gelöscht!')

def setup(bot):
    bot.add_cog(Admin(bot))
