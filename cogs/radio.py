import discord
import asyncio
from discord.ext import commands
from discord.commands import slash_command, Option, SlashCommandGroup, OptionChoice
from discord.utils import basic_autocomplete


async def radio_player(ctx: discord.AutocompleteContext):
    i = [
        OptionChoice("Trashpop", "https://streams.ilovemusic.de/iloveradio19.mp3"),
        OptionChoice("I Love Radio", "https://streams.ilovemusic.de/iloveradio1.mp3"),
        OptionChoice("2 Dance", "https://streams.ilovemusic.de/iloveradio2.mp3"),
        OptionChoice("2000+ Throwbacks", "https://streams.ilovemusic.de/iloveradio37.mp3"),
        OptionChoice("2010+ Throwbacks", "https://streams.ilovemusic.de/iloveradio38.mp3"),
        OptionChoice("Bass by HBZ", "https://streams.ilovemusic.de/iloveradio29.mp3"),
        OptionChoice("Chillhop", "https://streams.ilovemusic.de/iloveradio17.mp3"),
        OptionChoice("Dance 2023", "https://streams.ilovemusic.de/iloveradio36.mp3"),
        OptionChoice("Dance First!", "https://streams.ilovemusic.de/iloveradio103.mp3"),
        OptionChoice("Dance history", "https://streams.ilovemusic.de/iloveradio26.mp3"),
        OptionChoice("Deutschrap Beste", "https://streams.ilovemusic.de/iloveradio6.mp3"),
        OptionChoice("Deutschrap first!", "https://streams.ilovemusic.de/iloveradio104.mp3"),
        OptionChoice("Greatest hits", "https://streams.ilovemusic.de/iloveradio16.mp3"),
        OptionChoice("Hardstyle", "https://streams.ilovemusic.de/iloveradio21.mp3"),
        OptionChoice("Hip Hop", "https://streams.ilovemusic.de/iloveradio3.mp3"),
        OptionChoice("Hip Hop 2023", "https://streams.ilovemusic.de/iloveradio35.mp3"),
        OptionChoice("Hip Hop history", "https://streams.ilovemusic.de/iloveradio27.mp3"),
        OptionChoice("Hip Hop history", "https://streams.ilovemusic.de/iloveradio27.mp3"),
        OptionChoice("Hits 2023", "https://streams.ilovemusic.de/iloveradio109.mp3"),
        OptionChoice("Hits history", "https://streams.ilovemusic.de/iloveradio12.mp3"),
        OptionChoice("X-Max", "https://streams.ilovemusic.de/iloveradio8.mp3"),
        OptionChoice("The 90s", "https://streams.ilovemusic.de/iloveradio24.mp3"),
        OptionChoice("Party hard", "https://streams.ilovemusic.de/iloveradio14.mp3"),
        OptionChoice("1live", "https://wdr-1live-live.icecastssl.wdr.de/wdr/1live/live/mp3/128/stream.mp3"),
        OptionChoice("Antenne Bayern", "https://mp3channels.webradio.antenne.de/antenne"),
        OptionChoice("BigFM", "https://streams.bigfm.de/bigfm-deutschland-128-mp3"),
        OptionChoice("FHH", "https://mp3.ffh.de/radioffh/hqlivestream.mp3"),
        OptionChoice("HyFM Music 1", "https://mp3.ffh.de/radioffh/hqlivestream.mp3"),
        OptionChoice("HyFM Christmas Hits", "https://streams.hyfm.us/christmashits"),
        OptionChoice("HyFM Crossroads", "https://streams.hyfm.us/crossroads"),
        OptionChoice("HyFM Fireside Chill", "https://streams.hyfm.us/firesidechill"),
        OptionChoice("HyFM Late Night Drive", "https://streams.hyfm.us/latenightdrive"),
        OptionChoice("HyFM Pure Motivation", "https://streams.hyfm.us/puremotivation"),
        OptionChoice("HyFM Rap Life", "https://streams.hyfm.us/raplife"),
        OptionChoice("HyFM The New Seoul", "https://streams.hyfm.us/thenewseoul"),
        OptionChoice("HyFM Weekend Worthy", "https://streams.hyfm.us/weekendworthy"),
    ]
    
    return i

async def play_state_autocomplete(ctx: discord.AutocompleteContext):
    if ctx.interaction.guild.voice_client:
        if ctx.interaction.guild.voice_client.is_playing():
            return [OptionChoice("Pause", "pause")]
        else:
            return [OptionChoice("Resume", "resume")]


class Radio(commands.Cog):
    
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        
        self.v_clients = {}
        
    music = SlashCommandGroup("music", "Music commands")
        
    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(1.1)
        print("""
            radio.py         ✅""")
        
    @music.command(name="play_or_resume", description="Pause or resume playing")
    async def _play_state(self, ctx: discord.ApplicationContext, option: Option(str, "Resume or Pause", autocomplete=basic_autocomplete(play_state_autocomplete))):
        if option == "pause":
            vc: discord.VoiceClient = self.v_clients.get(ctx.guild.id)
            if not vc.is_playing():
                return await ctx.respond("Ich spiele garnix.", ephemeral=True)
            
            vc.pause()
            
            return await ctx.respond("Radio wurde pausiert.")
        
        elif option == "resume":
            vc: discord.VoiceClient = self.v_clients.get(ctx.guild.id)
            if not vc.is_paused():
                return await ctx.respond("Ich bin nicht pausiert.", ephemeral=True)
            
            vc.resume()
            
            return await ctx.respond("Ich spiele nun weiter Radio")
        
        else:
            return await ctx.respond("Das Radio hat irgendeinen Fehler schreibe in #bugs-und-report diesen Fehler", ephemeral=True)
        
    @music.command(name="radio", description="Play live radio")
    async def _join(self, ctx: discord.ApplicationContext):
        if not ctx.author.voice:
            return await ctx.respond("Wo soll ich spielen wenn du nicht in einem Voice Channel bist? <:pepemcs:866283900619063307> ", ephemeral=True)
        
        try:
            vc = await ctx.author.voice.channel.connect()
        except discord.errors.ClientException:
            ctx.guild.voice_client.cleanup()
            await ctx.guild.voice_client.disconnect()
            vc = await ctx.author.voice.channel.connect()
        
        self.v_clients[ctx.guild.id] = vc
        
        await ctx.respond("Ich bin nun bei dir")
        
    @music.command(name="stop", description="Stopt Live Radio")
    async def _stop(self, ctx: discord.ApplicationContext):
        if not ctx.author.voice:
            return await ctx.respond("Wie soll ich aufhören zu spielen wenn du nichtmal in einem Voice Channel bist? <:pepemcs:866283900619063307> ", ephemeral=True)
        
        vc: discord.VoiceClient = self.v_clients.get(ctx.guild.id)
        
        if not vc:
            return await ctx.respond("Ich bin nichtmal in einem Voice Channel.", ephemeral=True)
        
        if not vc.is_playing():
            return await ctx.respond("Ich spiele garnix.", ephemeral=True)
        
        vc.stop()
        await ctx.respond("Ich habe das Radio gestoppt.")
        
    @music.command(name="leave", description="Den Voice Channel verlassen")
    async def _leave(self, ctx: discord.ApplicationContext):
        if not ctx.author.voice:
            return await ctx.respond("Woher soll ich wissen aus welchen Voice Channel ich leaven soll wenn du nichtmal in einem Voice Channel bist? <:pepemcs:866283900619063307> ", ephemeral=True)
        
        vc: discord.VoiceClient = self.v_clients.get(ctx.guild.id)
        
        await vc.disconnect()
        await ctx.respond("Ich habe den Voice Channel verlassen.")
        
        vc.cleanup()
        
        self.v_clients.pop(ctx.guild.id)
        
    @music.command(name="play", description="Spielt Live Radio")
    async def _play(self, ctx: discord.ApplicationContext, radio: Option(str, "Suche dir ein Radio aus", autocomplete=basic_autocomplete(radio_player))):
        
        vc: discord.VoiceClient = self.v_clients.get(ctx.guild.id)
        
        if vc is None or ctx.author.voice.channel != vc.channel:
            if not ctx.author.voice:
                return await ctx.respond("Du bist in keinen Voice Channel.", ephemeral=True)
        
            try:
                vc = await ctx.author.voice.channel.connect()
            except discord.errors.ClientException:
                await ctx.guild.voice_client.disconnect()
                vc = await ctx.author.voice.channel.connect()
            
            self.v_clients[ctx.guild.id] = vc
        
        vc.stop()
        vc.play(discord.FFmpegPCMAudio(radio))
        
        return await ctx.respond("Ich spiele nun Radio. <a:pepeJAM:947951834180493372>")
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.id != self.bot.user.id:
            return
        
        vc: discord.VoiceClient = self.v_clients.get(member.guild.id)
        
        if not vc:
            return
        
        if after.channel is not None:
            after.self_deaf = True
            if vc.is_playing:
                vc.stop()
            return
        
        try:
            vc.cleanup()
        except:
            pass
        
        self.v_clients.pop(member.guild.id)


def setup(bot: discord.Bot):
    bot.add_cog(Radio(bot))