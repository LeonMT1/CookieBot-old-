import asyncio
import json
import os
import random
import time
import openai
from datetime import datetime

import aiosqlite
import discord
import humanfriendly
import pytz
import requests
from discord import Option, ui
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv

aktivitaet = discord.Activity(status=discord.Status.invisible)

activity = discord.Activity(type=discord.ActivityType.playing, name="mit Keksen")

bot = discord.Bot(intents=discord.Intents.all(), debug_guilds=None, activity=aktivitaet)
openai.api_key = "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"


@bot.event
async def on_ready():
    de = pytz.timezone('Europe/Berlin')
    print(f"{bot.user} ist nun online")
    online = discord.Embed(
        title='Wieder Online',
        description='Dieser Bot ist jetzt wieder online!',
        color=discord.Color.green(),
        timestamp=datetime.now().astimezone(tz=de))
    await asyncio.sleep(2)
    await bot.get_channel(825340653378338837).send(embed=online)
    for guild in bot.guilds:
        print(guild.name)


@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == 963728113920008212:
        if payload.message_id == 963735205917646878:
            if payload.emoji.name == "✅":
                guild: discord.Guild = bot.get_guild(724602228505313311)

                role: discord.Role = guild.get_role(724605752676843591)
                await payload.member.add_roles(role, reason="Zuweisung")
                channel: discord.TextChannel = guild.get_channel(963728113920008212)
                msg = await channel.send("Du hat jetzt vollen zugriff auf den Server Herzlichen Glückwunsch!")
                await asyncio.sleep(5)
                await msg.delete()


@bot.event
async def on_message(msg):
    print(msg.channel)
    print(msg.content)


player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


@bot.slash_command(description="Startet TicTacToe")
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    print(f"{ctx.author.name} hat /tictactoe gemacht")
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("Jetzt ist <@" + str(player1.id) + "> dran.")
        elif num == 2:
            turn = player2
            await ctx.send("Jetzt ist <@" + str(player2.id) + "> dran.")
    else:
        await ctx.send("Es wird greade gespielt warte bis das Spiel fertig ist!.")
    await ctx.respond(f"Es wurde erfolgreich TicTacToe gestartet", ephemeral=True)


@bot.slash_command(description="Platziert ein Feld bei TicTacToe")
async def place(ctx, pos: int):
    print(f"{ctx.author.name} hat /place gemacht")
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1

                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("Es ist gleichstand")

                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Bitte stelle sicher das du eine Zahl zwischen 1-9 eingibst.")
        else:
            await ctx.send("Du bist nicht am Zug.")
    else:
        await ctx.send("Starte mit ,tictactoe ein neues Spiel.")
    await ctx.respond(f'Zeichen wurde erfolgreich gesetzt')


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Trage bitte 2 Spieler ein (dich und deinen Gegner).")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "Bitte gehe sicher das du die Person getaggt hast mit der du Spielen willst (ie. <@688534433879556134>).")


@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Bitte gebe eine Position ein wo du dein x/o setzen willst.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Bitte stelle sicher eine ganze Zahl einzugeben.")


@bot.slash_command(description="Schicke eine Naricht")
@discord.default_permissions(administrator=True)
async def say(ctx, text: Option(str, "Den Text den du senden möchtest"), channel: Option(discord.TextChannel)):
    print(f"{ctx.author.name} hat /say gemacht")
    await channel.send(text)
    await ctx.respond("Die Naricht wurde erfolgreich Gesendet ✅", ephemeral=True)


@bot.slash_command(description="Die Magische Mies Muschel beantwortet jede deiner Fragen...")
async def miesmuschel(ctx, *, question):
    print(f"{ctx.author.name} hat /miesmuschel gemacht")
    ballresponse = ["Ja", "Nein", "Sicher", "Bestimmt", "SICHER NICHT", "nein du iditot", "Bitte bitte nicht",
                    "Bitte ja", "Wer weiß", "Ich weiß es nicht", "Frag jemanden anderes", "Lass mich in ruhe!",
                    "Ich kann mich nicht erinnern", "Du auch", "Bruh", "Hoffnung", "Nimm einfach einen Cookie"]
    answer = random.choice(ballresponse)
    await ctx.respond("Die Magische Mies Muschel überlegt...")
    async with ctx.typing():
        await asyncio.sleep(1)
    await ctx.respond(f"Du möchtest wissen **{question}**, ich sage dazu **{answer}**.")


@bot.slash_command(description="Hole deine Tägliche Portion Kekse ab (wenn du im Cookie Clan bist gibts extra hehe)")
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    async with aiosqlite.connect("level.db") as db:
        print(f"{ctx.author} hat /daily gemacht")
        cookies = random.randint(3, 10)
        cookiesmember = random.randint(3, 12)
        cookiesmemberplus = random.randint(3, 16)
        cookiesmembermod = random.randint(3, 20)
        cookiesmemberulti = random.randint(3, 24)
        guild = bot.get_guild(724602228505313311)
        member = guild.get_role(986320867518722068)
        memberplus = guild.get_role(986321038667309107)
        membermod = guild.get_role(986321161770119169)
        memberulti = guild.get_role(986321248210526208)
        embed = discord.Embed(title="Hier ist deine Tägliche Belohnung!",
                              description=f"Du hast deine Tägliche Belohnung von **{cookies}** Cookies abgeholt",
                              color=discord.Color.green())
        embedmember = discord.Embed(title="Hier ist deine Tägliche Belohnung!",
                                    description=f"Du hast deine Tägliche Belohnung von **{cookies}** Cookies abgeholt",
                                    color=discord.Color.green())
        embedmemberplus = discord.Embed(title="Hier ist deine Tägliche Belohnung!",
                                        description=f"Du hast deine Tägliche Belohnung von **{cookies}** Cookies abgeholt",
                                        color=discord.Color.green())
        embedmembermod = discord.Embed(title="Hier ist deine Tägliche Belohnung!",
                                       description=f"Du hast deine Tägliche Belohnung von **{cookies}** Cookies abgeholt",
                                       color=discord.Color.green())
        embedmemberulti = discord.Embed(title="Hier ist deine Tägliche Belohnung!",
                                        description=f"Du hast deine Tägliche Belohnung von **{cookies}** Cookies abgeholt",
                                        color=discord.Color.green())
        embedmember.set_footer(text="10% mehr durch Cookie Clan Member")
        embedmemberplus.set_footer(text="20% mehr durch Cookie Clan Member+")
        embedmembermod.set_footer(text="30% mehr durch Cookie Clan Mod")
        embedmemberulti.set_footer(text="40% mehr durch Cookie Clan Member Ultimate")

        if member in ctx.author.roles:
            await db.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", (cookiesmember,
                                                                                          ctx.author.name))
            await db.commit()
            await ctx.respond(embed=embedmember)
            return

        if memberplus in ctx.author.roles:
            await db.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", (cookiesmemberplus,
                                                                                          ctx.author.name))
            await db.commit()
            await ctx.respond(embed=embedmemberplus)
            return

        if membermod in ctx.author.roles:
            await db.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", (cookiesmembermod,
                                                                                          ctx.author.name))
            await db.commit()
            await ctx.respond(embed=embedmembermod)
            return

        if memberulti in ctx.author.roles:
            await db.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", (cookiesmemberulti,
                                                                                          ctx.author.name))
            await db.commit()
            await ctx.respond(embed=embedmemberulti)
            return

        await db.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", (cookies, ctx.author.name))
        await db.commit()
        await ctx.respond(embed=embed)


@bot.slash_command(description="Würfel! falls du mal keinen Würfel zur hand haben solltest.", name="würfeln")
async def wuerfeln(ctx):
    print(f"{ctx.author.name} hat /würfeln gemacht")
    wuerfelgif = "https://images-ext-1.discordapp.net/external/ci8_b281eob1YfQ-vPAKHQBBPSRt_xrA-7eYpd5d6As/https" \
                 "/media.tenor.com/IfbgWLbg_88AAAAC/dice.gif"
    zahl = random.randint(1, 6)
    await ctx.respond(f"{wuerfelgif}")
    async with ctx.typing():
        await asyncio.sleep(1)
    await ctx.respond(f"Du hast die Zahl {zahl} gewürfelt!")


@bot.slash_command(description="Zeige den Ping vom Bot an")
async def ping(ctx):
    print(f"{ctx.author.name} hat /ping gemacht")
    await ctx.respond(f"Pong - {round(bot.latency * 1000)}ms", ephemeral=True)


@bot.slash_command(description="Das kann der Bot")
async def funktionen(ctx):
    funktionen = discord.Embed(title="Funktionen", color=discord.Color.magenta(), description="""
Funktion: **/tictactoe**
Beschreibung: Spiele Tik Tak Toe
Beispiel:  /tictactoe p1:bsp p2:bsp
Rechte: Jeder

Funktion: **/place**
Beschreibung: Platziere dein Feld bei TicTacToe
Beispiel: /place pos:1
Rechte: Jeder

Funktion: **/say**
Beschreibung: Schreibe in jeden Channel eine belibige Naricht
Beispiel: /say text:Bsp channel:Bsp
Rechte: Nur Admins

Funktion: **/miesmuschel**
Beschreibung: Bekomme auf eine Frage eine Zuffälige antwort
Beispiel: /miesmuschel question:Bsp
Rechte: Jeder

Funktion: **/daily**
Beschreibung: Bekomme jede 24h Kekse
Beispiel: /daily
Rechte: Jeder (Cookie Member haben Vorteile)

Funktion: **/würfeln**
Beschreibung: Der Bot würfelt eine Zahl zwischen 1-6
Beispiel: /würfeln
Rechte: Jeder

Funktion: **/ping**
Beschreibung: Zeigt die Latenz zum Bot an
Beispiel: /ping
Rechte: Jeder

Funktion: **/funktionen**
Beschreibung: Zeigt eine Liste aller funktionen dieses Bots
Beispiel: /funktionen
Rechte: Jeder

Funktion: **/umfrage**
Beschreibung: Erstellt eine Umfrage
Beispiel: /umfrage args:bsp
Rechte: Admins

Funktion: **/timeout**
Beschreibung: Timeoutet leute
Beispiel: /timeout user:bsp time:1 reason:bsp
Rechte: Admin

Funktion: **/kick**
Beschreibung: Kickt Leute vom Server
Beispiel: /kick member:bsp
Rechte: Admin

Funktion: **/cr**
Beschreibung: Zeigt die Credits an
Beispiel: /cr
Rechte: Jeder

Funktion: **/clear**
Beschreibung: Löscht schnell viele Narichten
Beispiel: /clear amout:1
Rechte: Admin

Funktion: **/aktivität**
Beschreibung: Ändert die Aktivität vom Bot
Beispiel: /aktivität typ:stream name:bsp status:online streamer:bastighg
Rechte: Admin

Funktion: **/userinfo**
Beschreibung: Zeigt Infos über einen User an
Beispiel: /userinfo user:bsp
Rechte: Admin

Funktion: **Message Edit Log**
Beschreibung: Sobald jemand eine Naricht editiert sieht man dies im Modchat
Beispiel: Hans:Hallo(edited) Modchat:Hands:Hallq » edited: Hallo
Rechte: Mods

//command nicht fertig es ist greade nur 5uhr will endlich schlafen//""")
    await ctx.respond(embed=funktionen)


@bot.slash_command(description="Erstelle eine Umfrage in #infos")
async def umfrage(ctx, args):
    embed = discord.Embed(title=f"**NEUE UMFRAGE**!", description=f"""

       > **{args}** || @everyone ||

        """, color=discord.Color.green())
    embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
    await ctx.response.send_message(f"Deine Umfrage wurde gesendet ✅", ephemeral=True)
    channel = bot.get_channel(742699180623134772)
    msg = await channel.send(embed=embed)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')


@bot.slash_command(description="Timeoutet Leute")
async def timeout(ctx, user: discord.Member, time=None, *, reason=None):
    print(f"{ctx.author.name} hat /timeout gemacht")
    time = humanfriendly.parse_timespan(time)
    await user.timeout(until=discord.utils.utcnow() +
                             datetime.timedelta(seconds=time), reason=reason)
    await ctx.message.delete()

    em = discord.Embed(
        title="Erfolgreich",
        description=f"{user} wurde getimeoutet für {time}"
                    f"Sekunden Grund: {reason}",
        color=discord.Color.red()
    )
    em.set_footer(text=f'Angefordert von {ctx.author.name} • {ctx.author.id}')
    await ctx.send(embed=em)


@bot.slash_command(description="Kickt Leute")
@discord.default_permissions(administrator=True)
async def kick(ctx, member: Option(discord.Member, "Wähle einen Member")):
    print(f"{ctx.author.name} hat /kick gemacht")
    await member.kick()
    await ctx.respond(f"{member.mention} wurde gekickt!")


@bot.slash_command(description="Zeigt dir die Credits an")
async def cr(ctx):
    print(f"{ctx.author.name} hat /cr gemacht")
    de = pytz.timezone('Europe/Berlin')
    embed = discord.Embed(title=f'> Credits',
                          description='', color=0x4cd777, timestamp=datetime.now().astimezone(tz=de))
    embed.add_field(name='Coder', value=f'```LeonMT1 hat diesen Bot gecoded.```', inline=True)
    embed.add_field(name='Probleme und Tips',
                    value=f'```Bei bugs und Tips melde dich per dm bei LeonMT1#6088 oder tagge mich auf unseren Discord.```',
                    inline=True)
    embed.add_field(name='YT',
                    value=f'```Unser YT link ist: https://yotube.com/channel/UCafv4HJbRTFAfplelg7LUUQ```', inline=True)
    embed.add_field(name='Discord',
                    value=f'```Der Link zu unseren Community Discord: https://discord.gg/75Kh5vt.```', inline=True)
    embed.set_footer(text=f'Angefordert von {ctx.author.name} • {ctx.author.id}')
    await ctx.respond(embed=embed)


@bot.slash_command(deschripion="Löscht Narichten")
@discord.default_permissions(administrator=True)
async def clear(ctx, amout: int):
    global message_deleted
    print(f"{ctx.author.name} hat /clear gemacht")
    if amout > 1000:
        await ctx.send(f"Du kannst nicht mehr als 1000 Narichten auf einmal löschen !")
    else:
        count_members = {}
        messages = await ctx.channel.history(limit=amout).flatten()
        for message in messages:
            if str(message.author) in count_members:
                count_members[str(message.author)] += 1
            else:
                count_members[str(message.author)] = 1
        new_string = []
        messages_deleted = 0
        for author, message_deleted in list(count_members.items()):
            new_string.append(f'**{author}**: {message_deleted}')
            messages_deleted += message_deleted
        final_string = '\n'.join(new_string)
        await ctx.channel.purge(limit=amout + 1)
        await ctx.respond(f'Es wurden {message_deleted} Narichten gelöscht :white_check_mark: !\n\n{final_string}',
                          ephemeral=True)


@bot.event
async def on_application_command_error(ctx, error):
    print(f"Erorr {error}")
    await ctx.respond(f"Es ist ein Fehler aufgetreten: ```{error}```")
    raise error


def convert_time(seconds: int) -> str:
    if seconds < 60:
        return f"{round(seconds)} Sekunden"
    minutes = seconds / 60
    if minutes < 60:
        return f"{round(minutes)} Minuten"
    hours = minutes / 60
    return f"{round(hours)} Stunden"


@bot.event
async def on_application_command_error(ctx, error):
    print(f"Error {error}")
    if isinstance(error, commands.CommandOnCooldown):
        seconds = ctx.command.get_cooldown_retry_after(ctx)
        final_time = convert_time(seconds)

        await ctx.respond(f"Du musst noch {final_time} warten.", ephemeral=True)


@bot.slash_command(description="Aktivität vom Bot verändern", name="aktivität")
@commands.cooldown(1, 10, commands.BucketType.guild)
async def aktivitaet(ctx,
                     typ: Option(str, choices=["game", "stream"], description="Wähle eine Aktivität aus"),
                     name: Option(str, description="Schreibe hier den Namen der Aktiviät hin"),
                     status: Option(str, description="Welchen online Status soll der Bot haben?",
                                    choices=["online", "abwesend", "Bitte nicht Stören", "offline"]),
                     streamer: Option(str, default='https://twitch.tv/lado5670_lul',
                                      description="Gib hier den Kanalnamen ein (komplett klein)")
                     ):
    global act
    print(f"{ctx.author.name} hat /aktivität gemacht")
    if typ == "game":
        act = discord.Game(name=name)

    if typ == "stream":
        act = discord.Streaming(
            name=name,
            url=f"https://twitch.tv/{streamer}"
        )

    if status == "online":
        statusv = discord.Status.online

    await bot.change_presence(activity=act, status=statusv)
    await ctx.respond("Die Aktivität wurde erfolgreich geändert", ephemeral=True)


@bot.slash_command(description="Zeige dir Infos über diesen Server")
async def serverinfo(ctx):
    guild: discord.Guild = bot.get_guild(724602228505313311)
    time = discord.utils.format_dt(guild.created_at, "R")
    embed = discord.Embed(title=f"{guild.name} Infos", description=f"Hier siehst du alle Details über den Server "
                                                                   f"{guild.name}", color=discord.Color.random())
    embed.add_field(name="Name", value=f"{guild.name} • {guild.id}", inline=False)
    embed.add_field(name="Afk Channel", value=f"{guild.afk_channel} AFK Channel • {guild.afk_timeout} Timeout",
                    inline=False)
    embed.add_field(name="Member Count", value=f"{guild.member_count} Member", inline=False)
    embed.add_field(name="Owner", value=f"{guild.owner} • {guild.owner_id}", inline=False)
    embed.add_field(name="Erstellt", value=f"{time}", inline=False)
    embed.set_thumbnail(url=guild.icon.url)
    await ctx.respond(embed=embed)


@bot.slash_command(description="Zeige Infos über einen User")
async def userinfo(
        ctx,
        user: Option(discord.Member, "Gib einen User an", default=None), ):
    print(f"{ctx.author.name} hat /userinfo gemacht")
    if user is None:
        user = ctx.author

    embed = discord.Embed(
        title=f"Infos über {user.name}",
        description=f"Hier siehst du alle Details über {user.mention}",
        color=discord.Color.blue()
    )

    time = discord.utils.format_dt(user.created_at, "R")
    join = discord.utils.format_dt(user.joined_at, "R")

    embed.add_field(name='Name', value=f'{user.name}#{user.discriminator}', inline=False)
    embed.add_field(name='Nickname', value=f'{(user.nick if user.nick else "Nicht gesetzt")}', inline=False)
    embed.add_field(name="Account erstellt", value=time, inline=False)
    embed.add_field(name="Server beigetreten", value=join, inline=False)
    embed.add_field(name='Bot', value=f'{("Ja" if user.bot else "Nein")}', inline=False)
    embed.add_field(name='Rollen', value=f'{len(user.roles)}', inline=False)
    embed.add_field(name='Höchste Rolle', value=f'{user.top_role.name}', inline=False)
    embed.add_field(name='Farbe', value=f'{user.color}', inline=False)
    embed.add_field(name='Booster', value=f'{("Ja" if user.premium_since else "Nein")}', inline=False)

    embed.set_thumbnail(url=user.display_avatar.url)
    embed.set_footer(text=f'Angefordert von {ctx.author.name} • {ctx.author.id}')

    await ctx.respond(embed=embed)


@bot.event
async def on_message_delete(message):
    de = pytz.timezone('Europe/Berlin')
    em = discord.Embed(
        title='Messege Delete',
        description=f'**Gelöschte Nachricht von**: {message.author}'
                    f'\r\n**Inhalt der Nachricht**: {message.content}'
                    f'\r\n**Im Channel**: {message.channel.mention}',
        color=0xe74c3c,
        timestamp=datetime.now().astimezone(tz=de)
    )
    await bot.get_channel(825340653378338837).send(embed=em)


@bot.event
async def on_message_edit(before, after):
    de = pytz.timezone('Europe/Berlin')
    if before.author.bot:
        return

    embed = discord.Embed(title="Nachricht bearbeitet", color=discord.Color.blue(),
                          timestamp=datetime.now().astimezone(tz=de))

    embed.add_field(name="Vorher", value=before.content, inline=False)
    embed.add_field(name="Nachher", value=after.content, inline=False)
    embed.set_author(name=before.author.name, icon_url=before.author.avatar.url)
    embed.add_field(name="Kanal", value=before.channel.mention, inline=True)

    log_channel_id = 825340653378338837  # ID des Log-Channels einfügen
    log_channel = bot.get_channel(log_channel_id)
    await log_channel.send(embed=embed)


@bot.event
async def on_member_update(before, after):
    if len(before.roles) > len(after.roles):
        de = pytz.timezone('Europe/Berlin')
        role = next(role for role in before.roles if role not in after.roles)
        em = discord.Embed(
            title='Rollenänderung',
            description=f'**Name**: {before}\r\n**Entfernte Rolle:**: {role.name}',
            color=0xe91e63,
            timestamp=datetime.now().astimezone(tz=de)
        )

    elif len(after.roles) > len(before.roles):
        de = pytz.timezone('Europe/Berlin')
        role = next(role for role in after.roles if role not in before.roles)
        em = discord.Embed(
            title='Rollenänderung',
            description=f'**Name**: {before}\r\n**Neue Rolle:**: {role.name}',
            color=0x1f8b4c,
            timestamp=datetime.now().astimezone(tz=de)
        )

    elif before.nick != after.nick:
        de = pytz.timezone('Europe/Berlin')
        em = discord.Embed(
            title='Nickname wurde geändert!',
            description=f'**Name**: {before}\r\n**Alter NickName**: {before.nick}\r\n**Neuer NickName**: {after.nick}',
            color=0x3498db,
            timestamp=datetime.now().astimezone(tz=de)
        )

    else:
        return
    await bot.get_channel(825340653378338837).send(embed=em)


@bot.event
async def on_guild_channel_create(channel):
    de = pytz.timezone('Europe/Berlin')
    em = discord.Embed(
        title='Channel wurde erstellt',
        description=f'**Neuer Channel**: {channel.mention}',
        color=0x7289da,
        timestamp=datetime.now().astimezone(tz=de)
    )
    await bot.get_channel(825340653378338837).send(embed=em)


@bot.event
async def on_guild_channel_delete(channel):
    de = pytz.timezone('Europe/Berlin')
    em = discord.Embed(
        title='Channel wurde erstellt',
        description=f'**Channel wurde gelöscht**: {channel.mention}',
        color=0x546e7a,
        timestamp=datetime.now().astimezone(tz=de)
    )
    await bot.get_channel(825340653378338837).send(embed=em)


@bot.event
async def on_member_join(member):
    de = pytz.timezone('Europe/Berlin')
    em = discord.Embed(
        title='Member Joint',
        description=f'**Nutzer**: {member.name}',
        color=0x1f8b4c,
        timestamp=datetime.now().astimezone(tz=de)
    )
    await bot.get_channel(825340653378338837).send(embed=em)


@bot.event
async def on_member_remove(member):
    de = pytz.timezone('Europe/Berlin')
    em = discord.Embed(
        title='Member Leave',
        description=f'**Nutzer**: {member.name}',
        color=0xe67e22,
        timestamp=datetime.now().astimezone(tz=de)
    )
    await bot.get_channel(825340653378338837).send(embed=em)


@bot.event
async def on_member_join(member):
    de = pytz.timezone('Europe/Berlin')
    em = discord.Embed(
        title=':wave: Hallo! Cool das du hier her gefunden hast!',
        description=f'Hallo {member.mention} wir hoffen du hast viel Spaß auf diesen Server ;).',
        color=discord.Color.orange(),
        timestamp=datetime.now().astimezone(tz=de),
    )
    em.set_thumbnail(url=member.display_avatar.url)
    em.set_image(
        url="https://media.discordapp.net/attachments/825340653378338837/963556131551191070/ezgif-1-9da174320c.gif")
    await bot.get_channel(963739194331631637).send(embed=em)


@bot.event
async def on_member_remove(member):
    de = pytz.timezone('Europe/Berlin')
    em = discord.Embed(
        title=':wave: Tschau! Er war noch viel zu Jung um zu sterben',
        description=f'Tschau {member.mention} vieleicht kommst du ja irgenwann wieder.',
        color=discord.Color.red(),
        timestamp=datetime.now().astimezone(tz=de),
    )
    em.set_thumbnail(url=member.display_avatar.url)
    em.set_image(
        url="https://media.discordapp.net/attachments/825340653378338837/963556131769298954/ezgif-2-d70a849863.gif")
    await bot.get_channel(963739194331631637).send(embed=em)


@bot.slash_command(description="Erzeuge ein Embed")
@discord.default_permissions(administrator=True)
async def embed(ctx):
    print(f"{ctx.author.name} hat /embed gemacht")
    modal = embedModal(title="Mache ein Embed")
    await ctx.send_modal(modal)


class embedModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label="Embed Titel",
                placeholder="Schreibe hier!"),
            discord.ui.InputText(
                label="Embed Beschreibung",
                placeholder="Schreibe hier!",
                style=discord.InputTextStyle.long),
            *args,
            **kwargs)

    async def callback(self, interaction):
        de = pytz.timezone('Europe/Berlin')
        embed = discord.Embed(
            title=self.children[0].value,
            description=self.children[1].value,
            color=discord.Color.orange(),
            timestamp=datetime.now().astimezone(tz=de)
        )
        await interaction.response.send_message(embed=embed)


@bot.slash_command(description='Zeigt ein random deutsches meme von Reddit')
async def meme(ctx):
    async def delete_msg(inter):
        print(f"{ctx.author.name} hat /meme gemacht")
        if not inter.user == ctx.author:
            embed = discord.Embed(description=":warning: | Du hast das Menü nicht erstellt!", color=0xff7070)
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        await inter.message.delete()

    async def anoth(inter):
        if not inter.user == ctx.author:
            embed = discord.Embed(description=":warning: | Du hast das Menü nicht erstellt!", color=0xff7070)
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        embed = epic_meme()
        await inter.response.edit_message(embed=embed)

    view = View()
    anotherone = Button(label="Noch einen!", emoji="👍", style=discord.ButtonStyle.blurple)
    exit = Button(label="Löschen")
    anotherone.callback = anoth
    exit.callback = delete_msg
    view.add_item(anotherone)
    view.add_item(exit)
    embed = epic_meme()
    await ctx.respond(embed=embed, view=view)


def epic_meme():
    listreddit = ['memes', 'deutschememes', 'meme', 'OkBrudiMongo', 'scheissepfostieren', 'IchBin40UndLustig',
                  'IchBin40UndRechts', 'dankmemes']
    subreddit = random.choice(listreddit)
    count = 1
    timeframe = 'day'  # Hier alle timeframes: hour, day, week, month, year, all
    listing = 'random'  # Themen: controversial, best, hot, new, random, rising, top

    def get_reddit(subreddit, count):
        global request
        try:
            base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?count={count}&t={timeframe}'
            request = requests.get(base_url, headers={'User-agent': 'yourbot'})
        except:
            print('Ein Fehler ist aufgetreten!')
        return request.json()

    top_post = get_reddit(subreddit, count)

    title = top_post[0]['data']['children'][0]['data']['title']
    url = top_post[0]['data']['children'][0]['data']['url']
    ups = top_post[0]['data']['children'][0]['data']['ups']
    embed = discord.Embed(title=f":rofl: | {title}", color=discord.Color.random())
    embed.set_image(url=url)
    embed.set_footer(text=f"r/{subreddit} >> {ups} Upvotes")
    return embed


@bot.slash_command(description="Zeige ein gif von Tenor")
async def gif(ctx, search: Option(str, description="Schreibe hier das rein nach was der Bot suchen soll")):
    print(f"{ctx.author.name} hat /gif gemacht")
    key = "AIzaSyDHmg80hvYQrUvrTEee8ARuq9X-6hIE1EM"

    params = {"q": {search},
              "key": key,
              "limit": 30,
              "media_filter": "gif"}

    result = requests.get(f"https://tenor.googleapis.com/v2/search", params=params)
    data = result.json()

    number = random.randint(0, 30)

    url = data["results"][number]["media_formats"]["gif"]["url"]

    embed = discord.Embed(title=f"{search} Gif", color=discord.Color.random())
    embed.set_image(url=url)
    embed.set_footer(text="Von Tenor")
    await ctx.respond(embed=embed)


@bot.slash_command(description="Hole deine Zinsen ab!")
@commands.cooldown(1, 86400, commands.BucketType.user)
async def zinsen(ctx):
    async with aiosqlite.connect("level.db") as db:
        print(f"{ctx.author.name} hat /zinsen gemacht")
        de = pytz.timezone('Europe/Berlin')
        datum = datetime.now().astimezone(tz=de).strftime("%d")
        datum2 = 30 - int(datum)
        print(datum)
        if datum == 1:
            async with db.execute("SELECT cookies FROM users WHERE user_id = ?", (ctx.author.name,)) as cursor:
                result = await cursor.fetchone()
                zinsen = result[0] * 0.10
            await db.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", (zinsen, ctx.author.name))
            await db.commit()
            embederfolgreich = discord.Embed(title=f"10% Zinsen abgeholt!",
                                             description=f"Du hast deine Zinsen abgeholt!",
                                             color=discord.Color.green())
            embederfolgreich.add_field(name="Rechnung", value=f"""
Ehemaliger Konto stand: **{result[0]}**
Zinsen:                +**{zinsen}**
                        _______
Neuer Konto stand:     **{result[0] + zinsen}**""")
            await ctx.respond(embed=embederfolgreich)
            return

        embederfolgreich = discord.Embed(title="Keine Zinsen für dich!",
                                         description=f"Du kannst nur am 1. des Monats deine Zinsen abholen! "
                                                     f"Du kannst deine Zinsen in ca **{datum2} Tagen** abholen!",
                                         color=discord.Color.red())
        await ctx.respond(embed=embederfolgreich)


@bot.slash_command()
async def world_time(ctx, land: Option(str, description="Wähle ein Land aus", default=None)):
    print(f"{ctx.author.name} hat /time gemacht")
    if land is None:
        embed = discord.Embed(title="Diese Länder gibt es bei diesen Command!",
                              description="Deutschland, ️Afrika, Amerika, Antarctica, Arctic, Asia, Atlantic, Australia,"
                                          " Brazil, Canada, Chile, Cuba, Egypt, Eire, Greenwich, Hongkong, Iceland, "
                                          "Indian, Iran, Israel,Jamaica, Japan, Kwajalein, Libya, Mexico, Navajo, "
                                          "Pacific,Poland, Portugal, Singapore, Turkey, US, Zulu",
                              color=discord.Color.random())
        await ctx.respond(embed=embed)
        return
    if land == "Deutschland":
        land = pytz.timezone('Europe/Berlin')
    if land == "Afrika":
        land = pytz.timezone('Africa/Johannesburg')
    if land == "Amerika":
        land = pytz.timezone('America/New_York')
    if land == "Antarctica":
        land = pytz.timezone('Antarctica/Casey')
    if land == "Arctic":
        land = pytz.timezone('Arctic/Longyearbyen')
    if land == "Asia":
        land = pytz.timezone('Asia/Kolkata')
    if land == "Atlantic":
        land = pytz.timezone('Atlantic/Reykjavik')
    if land == "Australia":
        land = pytz.timezone('Australia/Sydney')
    if land == "Brazil":
        land = pytz.timezone('Brazil/East')
    if land == "Canada":
        land = pytz.timezone('Canada/Pacific')
    if land == "Chile":
        land = pytz.timezone('Chile/Continental')
    if land == "Cuba":
        land = pytz.timezone('Cuba')
    if land == "Egypt":
        land = pytz.timezone('Egypt')
    if land == "Eire":
        land = pytz.timezone('Eire')
    if land == "Greenwich":
        land = pytz.timezone('Greenwich')
    if land == "Hongkong":
        land = pytz.timezone('Hongkong')
    if land == "Iceland":
        land = pytz.timezone('Iceland')
    if land == "Indian":
        land = pytz.timezone('Indian/Christmas')
    if land == "Iran":
        land = pytz.timezone('Iran')
    if land == "Israel":
        land = pytz.timezone('Israel')
    if land == "Jamaica":
        land = pytz.timezone('Jamaica')
    if land == "Japan":
        land = pytz.timezone('Japan')
    if land == "Kwajalein":
        land = pytz.timezone('Kwajalein')
    if land == "Libya":
        land = pytz.timezone('Libya')
    if land == "Mexico":
        land = pytz.timezone('Mexico/BajaNorte')
    if land == "Navajo":
        land = pytz.timezone('Navajo')
    if land == "Pacific":
        land = pytz.timezone('Pacific/Guadalcanal')
    if land == "Poland":
        land = pytz.timezone('Poland')
    if land == "Portugal":
        land = pytz.timezone('Portugal')
    if land == "Singapore":
        land = pytz.timezone('Singapore')
    if land == "Turkey":
        land = pytz.timezone('Turkey')
    if land == "US":
        land = pytz.timezone('US/Eastern')
    if land == "Zulu":
        land = pytz.timezone('Zulu')
    embed = discord.Embed(title=f"Aktuelle Zeit {land}",
                          description=datetime.now().astimezone(tz=land).strftime("%H:%M:%S"),
                          color=discord.Color.random())
    embed.add_field(name=f"Aktuelles Datum {land}", value=datetime.now().astimezone(tz=land).strftime("%d.%m.%Y"))
    await ctx.respond(embed=embed)


@bot.event
async def on_message_delete(message: discord.Message):
    if message.mentions != 0:
        if len(message.mentions) < 3:
            for m in message.mentions:
                if m == message.author or m.bot:
                    pass
                else:
                    embed = discord.Embed(title=f"Ghost ping",
                                          description=f"{m} du wurdest von {message.author.mention} "
                                                      f"ghostpinged.\n \nNachricht: "
                                                      f"{message.content}",
                                          color=discord.Color.red())
                    await message.channel.send(embed=embed)
        else:
            embed2 = discord.Embed(title=f"Ghost ping", description=f"{len(message.mentions)} User wurden von "
                                                                    f"{message.author.mention} ghostpinged.\n \nNachrich"
                                                                    f"t:"
                                                                    f"{message.content}", color=discord.Color.red())
            await message.channel.send(embed=embed2)


@bot.slash_command(description="Startet Youtube in deinen Voicechannel")
async def youtube(ctx):
    print(f"{ctx.author.name} hat /youtube gemacht")
    if ctx.author.voice != None:
        channel = ctx.author.voice.channel
        invite = await channel.create_activity_invite(discord.EmbeddedActivity.watch_together, max_age=600,
                                                      reason="YT geöffnet")
        embed = discord.Embed(title="Aktivität geöffnet!",
                              description=f"[Du und deine Freunde können auf diesen Link klicken um gemeinsam "
                                          f"YT zu schauen]({invite.url})", color=discord.Color.dark_gold())
        if ctx.author.is_on_mobile:
            embed.add_field(name=":warning: Für Handy User:",
                            value="Aktivitäten funktionieren noch nicht auf dem Handy!", inline=True)
        embed.set_footer(text='Will expire after 600s!')
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(embed=discord.Embed(description=":warning: Du musst in einem VC sein!",
                                              color=discord.Color.red()))


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if member.bot:
        return

    call_length = 0
    async with aiosqlite.connect("level.db") as db:
        de = pytz.timezone('Europe/Berlin')
        embed2 = discord.Embed(
            title='Zeit im Talk',
            description=f'**Zeit im Talk**: {member.name} war {call_length}S im Talk',
            color=discord.Color.blurple(),
            timestamp=datetime.now().astimezone(tz=de)
        )
        with open('vc.json', 'r') as f:
            data = json.load(f)
        if not member.voice:
            try:
                call_length = round(time.time()) - data[str(member.id)]
                await db.execute("UPDATE users SET call_sec = call_sec + ? WHERE user_id = ?",
                                 (call_length, member.name))
                await db.commit()
                print(f"{member.name} war {call_length} Sekunden im Talk")
                embed2.description = f'**Zeit im Talk**: {member.name} war {call_length}S im Talk'
                await bot.get_channel(1079768281709301821).send(embed=embed2)
                del data[str(member.id)]
            except KeyError:
                return
        else:
            data[str(member.id)] = round(time.time())
        with open('vc.json', 'w') as f:
            json.dump(data, f)



@bot.slash_command(description='Narichten als anderer User schicken')
@discord.default_permissions(administrator=True)
async def sudo(ctx, user: Option(discord.Member), msg: Option(str, Required=True)):
    print(f"{ctx.author.name} hat /sudo gemacht")
    embed = discord.Embed(title="Sende Nachricht...",
                          color=discord.Color.green())
    await ctx.respond(embed=embed, ephemeral=True)
    webhook = await ctx.channel.create_webhook(name="Sudo webhook...", reason=f"Von: {ctx.author} Nachricht: {msg}")
    await webhook.send(username=f"{user.name}", avatar_url=f"{user.avatar.url}", content=f"{msg}")
    await webhook.delete()


@bot.slash_command(description="Einen Nutzer eine Bestimmt Role eine bestimmt Zeit geben")
@discord.default_permissions(administrator=True)
async def timedrole(ctx, member: discord.Member, role: discord.Role, zeit: Option(int, description="(in Sekunden "
                                                                                                   "angeben) Wie lange "
                                                                                                   "soll der Member "
                                                                                                   "die Rolle haben?")):
    print(f"{ctx.author.name} hat /timedrole gemacht")
    logchannel = bot.get_channel(825340653378338837)
    give = discord.Embed(title="Give Timedrole", color=discord.Color.green(), description=f"**{ctx.author.name}** hat "
                                                                                          f"**{member.name}** die Role "
                                                                                          f"**{role}** für {zeit} "
                                                                                          f"Sekunden gegeben")
    entgive = discord.Embed(title="Taked Timedrole", color=discord.Color.red(), description=f"**{member.name}** "
                                                                                            f"wurde die "
                                                                                            f"Timedrole genommen die er"
                                                                                            f" von **{ctx.author.name}"
                                                                                            f"** für **{zeit}** "
                                                                                            f"Sekunden hatte.")
    await member.add_roles(role)
    await ctx.respond(f"Du hast **{member.name}** erfolgreich die Role **{role}** für **{zeit}** Sekunden gegeben.")
    await bot.get_channel(logchannel).send(embed=give)
    await member.send(f"Du hast von **{ctx.author.name}** die Rolle **{role}** für **{zeit}** Sekunden bekommen.")
    await asyncio.sleep(zeit)
    await member.remove_roles(role)
    await bot.get_channel(logchannel).send(embed=entgive)
    await member.send(f"Die Rolle **{role}** wurde dir entzogen da die zeit von **{zeit}** vorbei ist.")


@bot.slash_command(name='reactionrole', description='Erstellt eine Reactionrole')
@discord.default_permissions(administrator=True)
async def rr(ctx, role: discord.Role):
    print(f"{ctx.author.name} hat /reactionrole gemacht")
    if not role.is_assignable:
        embed = discord.Embed(title=":warning: Bot hat keine Rechte um diese Rolle anderen zu geben!",
                              color=discord.Color.red())
        await ctx.respond(embed=embed, ephemeral=True)
        return
    else:
        class MyModal(discord.ui.Modal):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(
                    discord.ui.InputText(
                        label="Embed Titel",
                        placeholder="BSP. Reaction Roles",
                    ),
                    discord.ui.InputText(
                        label="Embed Beschreibung",
                        placeholder="BSP. Klicke hier für die Cookie Rolle!",
                        style=discord.InputTextStyle.long,
                    ),
                    *args,
                    **kwargs,
                )

            async def callback(self, interaction: discord.Interaction):
                de = pytz.timezone('Europe/Berlin')
                title = value = self.children[0].value
                desc = value = self.children[1].value
                embed = discord.Embed(title=f"{title}", description=f"{desc}", color=discord.Color.random(),
                                      timestamp=datetime.now().astimezone(tz=de))
                msg = await ctx.send(embed=embed)
                msg_id = msg.id
                with open('rr.json', 'r') as f:
                    rr = json.load(f)
                rr[str(msg_id)] = role.id
                with open('rr.json', 'w') as f:
                    rr = json.dump(rr, f)
                    msg = bot.get_message(msg_id)
                    await msg.add_reaction("✅")
                    embed2 = discord.Embed(title="Erfolgreich erstellt!", color=discord.Color.green())
                    await interaction.response.send_message(embed=embed2, ephemeral=True)

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
            if role is None or not role.is_assignable:
                _channel = discord.utils.get(guild.channels, id=payload.channel_id)
                await _channel.send('Ich habe keine Rechte um diese Rolle anderen zu geben oder sie wurde gelöscht!')
                return
            try:
                await member.add_roles(role)
            except discord.Forbidden:
                _channel = discord.utils.get(guild.channels, id=payload.channel_id)
                await _channel.send('Ich habe keine Rechte um diese Rolle anderen zu geben oder sie wurde gelöscht!')


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
                await _channel.send('Ich habe keine Rechte um diese Rolle anderen zu geben oder sie wurde gelöscht!')
            try:
                await member2.remove_roles(role)
            except discord.Forbidden:
                _channel = discord.utils.get(guild.channels, id=payload.channel_id)
                await _channel.send('Ich habe keine Rechte um diese Rolle anderen zu geben oder sie wurde gelöscht!')


@bot.event
async def on_message(message):
    # bug channel id ersetzen
    if message.author.bot:
        return
    if message.channel.id == 1071805141591793806:
        # mod chat channel ersetzten
        channel = bot.get_channel(1071805178312917105)
        embed = discord.Embed(title="**Neuer Bug:**", description=message.content)
        await channel.send(embed=embed, view=BugView(message.author))
        await message.delete()


class BugView(discord.ui.View):
    def __init__(self, user):
        self.user = user
        super().__init__(timeout=None)

    @discord.ui.button(label="✅", style=discord.ButtonStyle.green)
    async def button_callback1(self, button, interaction):
        async with aiosqlite.connect("level.db") as db:
            cookie = random.randint(10, 50)
            embeduser = discord.Embed(title="Bestätigt",
                                      description=f"Du hast durch das reporten eines Bugs/Reports **{cookie}** Cookies erhalten.",
                                      color=discord.Color.green())
            await interaction.response.send_message(f"Bug wurde bestätigt, der Member bekommt {cookie} Cookies")
            # Hier soll der User Cookies bekommen
            member = self.user
            await db.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", (cookie, self.user.name))
            # role id ersetzen
            role = discord.utils.get(member.guild.roles, id=1043532505887809577)
            if role not in member.roles:
                await member.send(embed=embeduser)
            else:
                return

    @discord.ui.button(label="❌", style=discord.ButtonStyle.green)
    async def button_callback2(self, button, interaction):
        embeduser = discord.Embed(title="Abgelehnt",
                                  description="Dein Bug/Report wurde nicht von unseren Mods angenommen.",
                                  color=discord.Color.red())
        await interaction.response.send_message("Bug/Report wurde nicht bestätigt, der Member bekommt keine Cookies.")
        member = self.user
        role = discord.utils.get(member.guild.roles, id=1043532505887809577)
        if role not in member.roles:
            await member.send(embed=embeduser)
        else:
            return


if __name__ == "__main__":
    bot.load_extension("cogs.lvlsystem")
    # bot.load_extension("cogs.knilzbot")
    bot.load_extension("cogs.bugreport")
    # bot.load_extension("cogs.mmosystem")
    # bot.load_extension("cogs.afk")
    # bot.load_extension("cogs.mathe")
    # bot.load_extension("cogs.ticketsystem")
    bot.load_extension("cogs.settings")
    # bot.load_extension("cogs.economy")
    bot.load_extension("cogs.mcstats")
    bot.load_extension("cogs.counting")
    bot.load_extension("cogs.radio")
    bot.load_extension("cogs.boosttime")
    bot.load_extension("cogs.warn")
    bot.load_extension("cogs.funcommands")
    load_dotenv()
    bot.run(os.getenv("TESTTOKEN"))
