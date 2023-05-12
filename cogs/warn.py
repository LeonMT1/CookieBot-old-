import asyncio
import sqlite3

import discord
from discord import slash_command
from discord.ext import commands


class WarnSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = sqlite3.connect('warnings.db')
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS warnings (
                                member_id INTEGER,
                                reason TEXT
                            )''')
        self.connection.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(1.3)
        print("""
            warn.py      ✅""")

    @slash_command(name="warn", description="Verwarne einen Benutzer")
    @discord.default_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member, reason=None):
        self.cursor.execute('INSERT INTO warnings (member_id, reason) VALUES (?, ?)', (member.id, reason))
        self.connection.commit()
        embed = discord.Embed(title=f'{member.mention} wurde verwarnt.', description=f'Grund: **{reason}**')
        embed.set_author(name=member.name, icon_url=member.avatar.url)
        ctx.respond(embed=embed)

        await self.check_timeout(member)

    async def check_timeout(self, member):
        self.cursor.execute('SELECT COUNT(*) FROM warnings WHERE member_id = ?', (member.id,))
        result = self.cursor.fetchone()
        warning_count = result[0]

        if warning_count >= 10:
            # role = discord.utils.get(member.guild.roles, name='Muted')
            await member.edit(mute=True)
            await member.send('Du hast 10 oder mehr Warnungen erhalten und wurdest für 1 Woche gemutet.')
            await asyncio.sleep(604800)  # 1 Woche in Sekunden
            await member.edit(mute=False)

    @slash_command(name="warnings", description="Zeige alle Warnungen für einen Benutzer")
    async def warnings(self, ctx, member: discord.Member):
        self.cursor.execute('SELECT reason FROM warnings WHERE member_id = ?', (member.id,))
        result = self.cursor.fetchall()

        if result:
            embed = discord.Embed(title=f'Warnungen für {member.name}', color=discord.Color.red())
            for idx, row in enumerate(result):
                embed.set_author(name=member.name, icon_url=member.avatar.url)
                embed.add_field(name=f'Warnung {idx + 1}', value=row[0], inline=False)
            await ctx.respond(embed=embed)
        else:
            embed2 = discord.Embed(title=f'Es gibt keine Warnungen für {member.name}', color=discord.Color.green())
            embed2.set_author(name=member.name, icon_url=member.avatar.url)
            await ctx.respond(embed=embed2)

    @slash_command(name="warning_leaderboard", description="Zeige das Warnungs-Leaderboard")
    async def leaderboard(self, ctx):
        self.cursor.execute('SELECT member_id, COUNT(*) FROM warnings GROUP BY member_id ORDER BY COUNT(*) DESC')
        result = self.cursor.fetchall()

        if result:
            embed = discord.Embed(title='Warnungs-Leaderboard', color=discord.Color.gold())
            for idx, row in enumerate(result):
                member = ctx.guild.get_member(row[0])
                warnings_count = row[1]
                embed.add_field(name=f'Platz {idx + 1}: {member.name}', value=f'Anzahl der Warnungen: {warnings_count}',
                                inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Keine Warnungen auf diesen Server gefunden.')

    @slash_command(name="clear_warnings", description="Lösche alle Warnungen für einen Benutzer")
    @discord.default_permissions(administrator=True)
    async def clear_warnings(self, ctx, member: discord.Member):
        self.cursor.execute('DELETE FROM warnings WHERE member_id = ?', (member.id,))
        self.connection.commit()
        await ctx.respond(f'Warnungen für {member.mention} wurden gelöscht.')


def setup(bot):
    bot.add_cog(WarnSystem(bot))
