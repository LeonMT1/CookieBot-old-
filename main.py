import asyncio
import json
import os
import random
import time
from datetime import datetime

import aiosqlite
import discord
import humanfriendly
import pytz
import requests
from discord import Option
from discord.ext import commands, tasks
from discord.ui import Button, View
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

activity = discord.Activity(type=discord.ActivityType.playing, name="mit Keksen")

bot = discord.Bot(intents=intents, debug_guilds=[1016436920965939280, 724602228505313311], activity=activity)

# © 2022 - Martin B. ツ#2128
GUILD = 1016436920965939280
STATUS_ROLE = 1033889262246035456
STATUS_TEXT = "https://discord.gg/yaVeqUPhVE"
LOG_CHANNEL = 1016436921750270034


@bot.event
async def on_ready():
    de = pytz.timezone('Europe/Berlin')
    print(f"{bot.user} ist nun online")
    online = discord.Embed(
        title='Wieder Online',
        description='Dieser Bot ist jetzt wieder online!',
        color=discord.Color.green(),
        timestamp=datetime.now().astimezone(tz=de))
    vanity_task.start()
    await bot.get_channel(825340653378338837).send(embed=online)


async def has_vanity(member: discord.Member):
    if not len(member.activities) == 0:
        for i in member.activities:
            if isinstance(i, discord.CustomActivity):
                if STATUS_TEXT in i.name or STATUS_TEXT == i.name:
                    return True

    else:
        return False


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
        cookies = random.randint(3, 6)
        cookiesmember = random.randint(3, 8)
        cookiesmemberplus = random.randint(3, 9)
        cookiesmembermod = random.randint(3, 10)
        cookiesmemberulti = random.randint(3, 11)
        guild = bot.get_guild(724602228505313311)
        member = guild.get_role(986320867518722068)
        memberplus = guild.get_role(986321038667309107)
        membermod = guild.get_role(986321161770119169)
        memberulti = guild.get_role(986321248210526208)

        if member in ctx.author.roles:
            await db.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", (cookiesmember,
                                                                                          ctx.author.name))
            await db.commit()
            await ctx.respond(
                f"Du hast deine Tägliche Belohnung eingesammelt und **{cookiesmember}** Cookies bekommen! "
                f"(10% mehr durch Cookie Clan Member)")
            return

        if memberplus in ctx.author.roles:
            await db.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", (cookiesmemberplus,
                                                                                          ctx.author.name))
            await db.commit()
            await ctx.respond(
                f"Du hast deine Tägliche Belohnung eingesammelt und **{cookiesmemberplus}** Cookies bekommen! "
                f"(20% mehr durch Cookie Clan Member+)")
            return

        if membermod in ctx.author.roles:
            await db.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", (cookiesmembermod,
                                                                                          ctx.author.name))
            await db.commit()
            await ctx.respond(
                f"Du hast deine Tägliche Belohnung eingesammelt und **{cookiesmembermod}** Cookies bekommen! "
                f"(30% mehr durch Cookie Clan Mod)")
            return

        if memberulti in ctx.author.roles:
            await db.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", (cookiesmemberulti,
                                                                                          ctx.author.name))
            await db.commit()
            await ctx.respond(
                f"Du hast deine Tägliche Belohnung eingesammelt und **{cookiesmemberulti}** Cookies bekommen! "
                f"(40% mehr durch Ultimativer Cookie Member)")
            return

        await db.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", (cookies, ctx.author.name))
        await db.commit()
        await ctx.respond(f"Du hast deine Tägliche Belohnung eingesammelt und **{cookies}** Cookies bekommen!")


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
    em = discord.Embed(
        title='Messege Edit',
        description=f'**Bearbeitete Nachricht von**: {before.author}'
                    f'\r\n**Alte Nachricht**: {before.content}'
                    f'\r\n**Neue Nachricht**: {after.content}',
        color=0xf1c40f,
        timestamp=datetime.now().astimezone(tz=de)
    )
    await bot.get_channel(825340653378338837).send(embed=em)


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
    async with aiosqlite.connect("level.db") as db:
        de = pytz.timezone('Europe/Berlin')
        with open('vc.json', 'r') as f:
            data = json.load(f)
        if not member.voice:
            try:
                call_length = round(time.time()) - data[str(member.id)]
                embed = discord.Embed(
                    title='Zeit im Talk',
                    description=f'**Zeit im Talk**: {member.name} war {call_length}S im Talk',
                    color=discord.Color.blurple(),
                    timestamp=datetime.now().astimezone(tz=de)
                )
                await db.execute("UPDATE users SET call_sec = call_sec + ? WHERE user_id = ?",
                                 (call_length, member.name))
                await db.commit()
                print(f"{member.name} war {call_length} Sekunden im Talk")
                del data[str(member.id)]
            except KeyError:
                return
        else:
            data[str(member.id)] = round(time.time())
        with open('vc.json', 'w') as f:
            data = json.dump(data, f)
            await bot.get_channel(825340653378338837).send(embed=embed)


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
            if role == None or not role.is_assignable:
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

# @bot.slash_command(description="Reporte einen Bug")
# async def reportbug(ctx):

   # class bugModal(discord.ui.Modal):
       # def __init__(self, *args, **kwargs):
           # super().__init__(
               # discord.ui.InputText(
               #     label="Bug Titel",
              #      placeholder="zB: /event fehler!"),
             #   discord.ui.InputText(
            #        label="Bug Beschreibung",
           #         placeholder="zB: Wenn ich /event mache steht da ein Fehler!",
          #          style=discord.InputTextStyle.long),
         #       *args,
        #        **kwargs)

       # async def callback(self, interaction: discord.Interaction):
           # de = pytz.timezone('Europe/Berlin')
           # embed = discord.Embed(
            #    title=f"Bug Report von **LÜCKE** | Titel: **{self.children[0].value}**",
           #     description=self.children[1].value,
          #      color=discord.Color.red(),
         #       timestamp=datetime.now().astimezone(tz=de))
        #    message = await interaction.response.send_message(embed=embed)
       #     messageid = message.id
      #      print(messageid)
     #       await message.add_reaction("✅")
    #        await message.add_reaction("❌")

   # modal = bugModal(title="Reporte einen Bug!")
   # await ctx.send_modal(modal)


@tasks.loop(seconds=1)
async def vanity_task():
    await bot.wait_until_ready()

    guild: discord.Guild = bot.get_guild(GUILD)
    role = guild.get_role(STATUS_ROLE)
    log = bot.get_channel(LOG_CHANNEL)

    if guild.members:
        for member in guild.members:
            if member.bot:
                continue
            vanity = await has_vanity(member)
            if vanity:
                if not role in member.roles:
                    await member.add_roles(role, atomic=True)
                    embed = discord.Embed(
                        title="Vanity-Rolle hinzugefügt!",
                        description=f"{member.mention} hat die Vanity-Rolle **{role.mention}** erhalten.",
                        color=discord.Color.green()
                    )
                    await log.send(embed=embed)

            else:
                if role in member.roles:
                    await member.remove_roles(role, atomic=True)
                    embed = discord.Embed(
                        title="Vanity-Rolle entfernt!",
                        description=f"{member.mention} wurde die Vanity-Rolle {role.mention} entfernt.",
                        color=discord.Color.red()
                    )
                    await log.send(embed=embed)

if __name__ == "__main__":
    bot.load_extension("cogs.lvlsystem")
    # bot.load_extension("cogs.knilzbot")
    # bot.load_extension("cogs.admin")
    # bot.load_extension("cogs.mmosystem")
    # bot.load_extension("cogs.afk")
    # bot.load_extension("cogs.games")
    bot.load_extension("cogs.funcommands")
    load_dotenv()
    bot.run(os.getenv("TESTTOKEN"))
