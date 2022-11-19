import asyncio
import random
import aiosqlite

import discord
import requests
from discord import slash_command
from discord.ext import commands
import discord.commands


class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(0.8)
        print("""
            funcommands.py   ✅
            ------------------------""")

    @slash_command(description="Schlage jemanden")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def slap(self, ctx, member: discord.Member):
        guild: discord.Guild = self.bot.get_guild(724602228505313311)
        muterolle: discord.Role = guild.get_role(1043532505887809577)
        key = "AIzaSyDHmg80hvYQrUvrTEee8ARuq9X-6hIE1EM"
        params = {"q": "slap",
                  "key": key,
                  "limit": 30,
                  "media_filter": "gif"}

        result = requests.get(f"https://tenor.googleapis.com/v2/search", params=params)
        data = result.json()

        number = random.randint(0, 30)

        url = data["results"][number]["media_formats"]["gif"]["url"]

        if member == "Cookie Manager#9104":
            print(member)
            embot = discord.Embed(title="Ich bekomme alles mit!", color=discord.Color.orange(),
                                  description="Der Bot so krass, das du in nicht schlagen kannst!")
            embot.set_footer(text="Gif von Tenor")
            embot.set_image(
                url="https://images-ext-2.discordapp.net/external/ZLjKGm6-I9EJNnCpHUMu-J1ChjOhbuRUuqVR_p7dYhY/https/"
                    "media.tenor.com/FLGynS-9GqQAAAPo/will-smith-south-park.mp4")

        embed = discord.Embed(title=f"{ctx.author.name} hat {member} geschlagen!", color=discord.Color.red())
        embed.set_image(url=url)
        embed.set_footer(text="Gif von Tenor")
        print(f"{ctx.author.name} hat den Befehl /slap genutzt")
        await ctx.respond(embed=embed)
        geschlagen = discord.Embed(title=f"{ctx.author} hat dich geschlagen!", color=discord.Color.red(),
                                   description=f"RÄCHE DICH JETZT INDEM DU auf den **DER COOKIE CLAN** DC gehst und in "
                                               f"https://discord.com/channels/724602228505313311/963740046995890176 "
                                               f"/slap {ctx.author} machst 😉")
        if muterolle not in ctx.author.roles:
            await member.send(embed=geschlagen)

    @slash_command(description="Löse ein zufälliges Event aus. uiii")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def event(self, ctx):
        async with aiosqlite.connect("level.db") as db:
            print(f"{ctx.author} hat /event gemacht")
            guild: discord.Guild = self.bot.get_guild(724602228505313311)
            hodenkrebsrole: discord.Role = guild.get_role(1037153279886503967)
            hodenkrebs = random.randint(1, 1000)
            goodordosent = random.randint(1, 2)
            cookies = random.randint(1, 7)
            cookiesmuell = cookies + random.randint(1, 5)
            user = guild.members
            eventgood = [f"Du hast eine Packung Cookies auf der Straße gefunden du hast dich umgeschaut ob dich jemand "
                         f"beobachtet... Als du festgestellt hat das dich niemand beobachtet hast du Lachend alle "
                         f"Cookies mitgenommen es waren **{cookies}** Cookies.", f"Du hast im Aldilie eine Cookie "
                                                                                 f"Packung geklaut allerdings hat dich "
                                                                                 f"der Ladenbesitzer erwischt. Aber da "
                                                                                 f"er mitleid hatte hast du "
                                                                                 f"**{cookies}** Cookies bekommen.",
                         f"Du hast auf Onlycookies ein neues Video hochgeladen du wurdest allerdings gehackt aber du "
                         f"konntest trozdem **{cookies}** Cookies bekommen.",
                         f"Du hast einer Alten Oma über die Straße geholfen. Aus ihrer Tasche sind wärendesen {cookies}"
                         f" Cookies gefallen. Du hast alle vor ihren Augen eingesammelt und bist abgehauen.",
                         f"Du bist nach Hause gegangen und hast im Müll etwas Cookie Artiges gesehen du hast geschaut "
                         f"und es waren tatsächlich **{cookiesmuell}** Cookies im Müll du hollst alle raus und hast "
                         f"jetzt **{cookies}** Cookies mehr, da {cookiesmuell - cookies} schlecht waren.",
                         f"Du hast deine Cookies gezählt wie jeden morgen weil am Tag vorher {random.choice(user)} da "
                         f"war. Dann hast du festgestellt das sie dir **{cookies} dagelassen hat"]

            eventnotgood = [f"Du hast Elon Musk nach Twitter+ gefragt, er hatte dich mit seinem Waschbeken beworfen "
                            f"und dir sind **{cookies}** Cookies zerbrochen.", f"Du hast das neue Cyberpunk 2089 "
                                                                               f"gekauft allerdings ist es voller Bugs "
                                                                               f"und du raget und zerbichst "
                                                                               f"**{cookies}** Cookies dabei.",
                            f"Du hast im Aldilie eine Cookie Packung geklaut allerdings hat dich der Ladenbesitzer "
                            f"erwischt. Er hat dich verklagt und du musstest **{cookies}** Cookies strafe zahlen.",
                            f"Du bist auf den Bürgersteig hingefallen da du noch Cookies in deiner Hosentasche hattest "
                            f"sind **{cookies}** Cookies rausgerollt und wurden von einem Auto überfahren",
                            f"Du hast deine Cookies gezählt wie jeden morgen weil am Tag vorher {random.choice(user)} "
                            f"da war. Dann hast du festgestellt das sie dir **{cookies} hinterhältig geklaut hat!"]
            hodenkrebsembed = discord.Embed(title=f"{ctx.author.name} HAT HODENKREBS!", description="Du hast Absofort "
                                                                                                    "Hodenkrebs...",
                                            color=discord.Color.red())

            eventgoodembed = discord.Embed(title=f"{ctx.author.name} ist etwas **gutes** passiert...",
                                           description=random.choice(eventgood), color=discord.Color.green())

            eventnotgoodembed = discord.Embed(title=f"{ctx.author.name} ist etwas **schlechtes** passiert...",
                                              description=random.choice(eventnotgood), color=discord.Color.red())
            if hodenkrebs == 1000:
                await ctx.respond(embed=hodenkrebsembed)
                await ctx.author.add_roles(hodenkrebsrole)
                return
            if goodordosent == 1:
                await ctx.respond(embed=eventgoodembed)
                await db.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", (cookies, ctx.author.name))
                await db.commit()
                return
            await ctx.respond(embed=eventnotgoodembed)
            await db.execute("UPDATE users SET cookies = cookies - ? WHERE user_id = ?", (cookies, ctx.author.name))
            await db.commit()

    @slash_command(description="Hacke andere User für Kekse hehe")
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def hack(self, ctx, *, member: discord.Member):
        async with aiosqlite.connect("level.db") as db:
            print(f"{ctx.author} hat /hack gemacht")
            guild: discord.Guild = self.bot.get_guild(724602228505313311)
            muterolle: discord.Role = guild.get_role(1043532505887809577)
            async with db.execute("SELECT cookies FROM users WHERE user_id = ?", (member.name,)) as cursor:
                result = await cursor.fetchone()
            if result == 0:
                ehre = discord.Embed(title="Der Nutzer hat keine Erhackbaren Kekse!",
                                     description=f"{member.name} hat keine Kekse dadurch hast du die Bank gehackt diese"
                                                 f" hat dir die Polizei auf den Hals gejagt. Dadurch hast du **5** "
                                                 f"Cookies Verloren!")
                await ctx.respond(embed=ehre)
                await db.execute("UPDATE users SET cookies = cookies - 5 WHERE user_id = ?", (ctx.author.name,))
                await db.commit()
                return
            if member is ctx.author:
                dumm = discord.Embed(title="Kann es sein das du dumm bist?", description="Du hast auf Google nach den "
                                                                                         "besten Hacker Tools gesucht "
                                                                                         "und Virus.exe gefunden & "
                                                                                         "heruntergeladen. Hast die "
                                                                                         "datei allerdings selbst "
                                                                                         "geöffnet. Dabei hast du "
                                                                                         "**2** Cookies verloren.",
                                     color=discord.Color.red())
                await ctx.respond(embed=dumm)
                await db.execute("UPDATE users SET cookies = cookies - 2 WHERE user_id = ?", (ctx.author.name,))
                await db.commit()
                return
            opfer = member.name
            emails = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "_2000",
                      "_2001",
                      "_2002", "_2003", "_2004", "_2005", "_2006", "_2007", "_2008", "_2009", "_2010", "müller",
                      "_müller",
                      "Müller", "_Müller", "schmidt", "_schmidt", "Schmidt", "_Schmidt", "schneider", "_schneider",
                      "Schneider",
                      "_Schneider", "fischer", "Fischer", "_fischer", "_Fischer", "Weber", "weber", "_weber", "_Werber",
                      "Meyer", "meyer", "_Meyer", "_meyer", "Wagner", "wagner", "_Wagner", "_wagner", "becker",
                      "Becker",
                      "_becker", "_Becker", "Thiel", "thiel", "_thiel", "_Thiel"]
            passwords = ["hallo", "passwort", "hallo123", "schalke04", "passwort1", "qwertz", "arschl****", "schatz",
                         "fi****", "password", "12345678", "123456789", "baseball", "footbal", "qwertzuiop",
                         "1234567890",
                         "superman", "1qwz2wsx", "trustno1", "jennifer", "sunshine", "iloveyou", "starwars", "computer",
                         "michelle", "11111111", "princess", "987654321", "corvette", "1234qwer", "88888888",
                         "q1w2e3r4t5",
                         "internet", "samantha", "whatever", "maverick", "steelers", "mercedes", "123123123",
                         "qwer1234",
                         "hardcore", "midnight", "bigdaddy", "victoria", "cocacola", "marlboro", "asdfasdf",
                         "jaordan32",
                         "jonathan"]
            cookies = random.randint(0, 3)
            fa = ["an", "aus"]
            anbieter = ["PornHub", "Microsoft", "Riotgames", "Ubisoft", "Discord", "Rewe", "Lidl", "Netto", "Steam",
                        "Epic Games", "LeonMT1"]
            email = ["@gmail.com", "@outlook.de", "@yahoo.com", "@gmx.de", "@t-online.de", "@web.de"]

            await ctx.respond("Hack wird gestartet")
            message = await ctx.send(f"{member.name} wird jetzt gehackt...")
            await asyncio.sleep(2)
            await message.edit(content=f"[▘]Keks Konto login wurde gefunden... (2fa {random.choice(fa)})")
            await asyncio.sleep(3)
            await message.edit(content=f"""[▖]
        Email: {member.name}{random.choice(emails)}{random.choice(email)}
        Password: {random.choice(passwords)}""")
            await asyncio.sleep(3)
            await message.edit(content=f"[▝]Häufigste Überweisungs Anbieter: {random.choice(anbieter)}")
            await asyncio.sleep(3)
            await message.edit(content=f"[▘]Lädt...")
            await asyncio.sleep(3)
            await message.edit(content=f"[▖]Sucht IP...")
            await asyncio.sleep(3)
            await message.edit(content=f"[▝] IP: 49.124.134")
            await asyncio.sleep(3)
            await message.edit(content=f"Fertig mit dem Hack auf {member.mention}")
            await asyncio.sleep(2)
            await db.execute("UPDATE users SET cookies = cookies + ? WHERE user_id = ?", (cookies, ctx.author.name))
            await db.execute("UPDATE users SET cookies = cookies - ? WHERE user_id = ?", (cookies, opfer))
            await db.commit()
            if cookies == 0:
                await message.edit(content="Der Hack ist leider fehlgeschlagen")
                return
            embed = discord.Embed(title="Erfolgreich abgeschloßen!", description=f"""
Du hast von **{member.mention}** **{cookies}** Cookies erhackt!
Email: {member.name}{random.choice(emails)}{random.choice(email)}
Password: {random.choice(passwords)}
2FA Status: {random.choice(fa)}
Häufigeste Überweisung an: {random.choice(anbieter)}
Kontostand: {result[0]} Cookies""", color=discord.Color.green())
            embed.set_thumbnail(url=ctx.author.display_avatar.url)
            await message.edit(embed=embed)
            if muterolle not in member.roles:
                await member.send(f"""Du wurdest von {ctx.author} gehackt, er hat dir {cookies} Cookies geklaut xD.
Du kannst auch alle 12h jemand anderen Hacken und davon Cookies bekommen!""")


def setup(bot):
    bot.add_cog(FunCommands(bot))
