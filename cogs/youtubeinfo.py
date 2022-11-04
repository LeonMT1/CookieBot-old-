import asyncio
import json

import discord
from colorama import *
from discord.commands import slash_command
from discord.ext import commands, tasks
from pytube import Channel


class YouTubeBenarichtigung(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(0.2)
        print("""
            youtubeinfo.py  ✅""")
        self.checkforvideos.start()

        @tasks.loop(seconds=60)
        async def checkforvideos():
            with open("youtubedata.json", "r") as f:
                data = json.load(f)

            print(Fore.RED + "---------------Prüfe YouTube-Daten!---------------")

            for youtube_channel in data:
                print(
                    Fore.BLUE + f"----------Prüfe YouTube-Daten von {data[youtube_channel]['channel_name']}----------")
                channel = f"https://www.youtube.com/channel/{youtube_channel}"

                c = Channel(channel)
                try:
                    latest_video_url = c.video_urls[0]
                except:
                    continue

                if not str(data[youtube_channel]["latest_video_url"]) == latest_video_url:
                    data[str(youtube_channel)]['latest_video_url'] = latest_video_url

                    with open("youtubedata.json", "w") as f:
                        json.dump(data, f)

                    discord_channel_id = data[str(youtube_channel)]['notifying_discord_channel']
                    discord_channel = self.bot.get_channel(int(discord_channel_id))
                    msg = f"{data[str(youtube_channel)]['channel_name']} hat gerade ein Video hochgeladen: " \
                          f"{latest_video_url} "
                    await discord_channel.send(msg)

        # SlashCommand erstellen um mehr YouTube Accounts hinzuzufügen
        @slash_command(description="Füge einen YouTuber zu den Benachrichtigungen hinzu!")
        @discord.default_permissions(administrator=True)
        @discord.guild_only()
        async def add_yt_notify(ctx, channel_id: str, *, channel_name: str, discord_channel_id: str):
            with open("youtubedata.json", "r") as f:
                data = json.load(f)

            data[str(channel_id)] = {}
            data[str(channel_id)]["channel_name"] = channel_name
            data[str(channel_id)]["latest_video_url"] = "none"
            data[str(channel_id)]["notifying_discord_channel"] = discord_channel_id

            with open("youtubedata.json", "w") as f:
                json.dump(data, f)

            await ctx.respond("Daten hinzugefügt!", ephemeral=True)


def setup(bot):
    bot.add_cog(YouTubeBenarichtigung(bot))
