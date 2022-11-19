from discord.ext import commands
import discord
from datetime import datetime
import asyncio
from discord.ui import Button


class Ticket(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.add_view(VIEWNAME())

    @commands.command()
    @discord.default_permissions(administrator=True)
    async def tickets(self, ctx):
        em = discord.Embed(
            title='dbxFlame open source | Tickets',
            description=f'To create a Ticket click the Dropdown box below.\nSelect a Ticket Topic of your Choice to create a Ticket.',
            color=discord.Color.light_gray())
        await ctx.send('send')

        channel = self.client.get_channel(
            1018274183643402327)  # füge die Channel ID ein, wo die Ticket Nachricht mit dem Dropdown Menu geschickt werden soll
        await channel.send(embed=em, view=VIEWNAME())


def setup(client):
    client.add_cog(Ticket(client))


options = [
    discord.SelectOption(label='Ticket 1', description='Desc of Ticket 1', emoji='📩', value='1'),
    discord.SelectOption(label='Ticket 2', description='Desc of Ticket 2', emoji='📩', value='2'),
    discord.SelectOption(label='Ticket 3', description='Desc of Ticket 3', emoji='📩', value='3')
]


class VIEWNAME(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder='Select a Ticket topic',
        options=options,
        custom_id='Ticket'
    )
    async def select_callback(self, select, interaction):
        member = interaction.user
        client = interaction.client

        if '1' in interaction.data['values']:
            cat = client.get_channel(123456789)  # füge die Categorie ID ein, wo die Tickets erstellt werden sollen

            ticket_channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}',
                                                                         category=cat,
                                                                         topic=f'Ticket by {interaction.user} \nClient-ID: {interaction.user.id}')
            await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True,
                                                 view_channel=True)
            await ticket_channel.set_permissions(interaction.guild.default_role, view_channel=False)
            try:
                em1 = discord.Embed(
                    title='📬 Ticket open!',
                    description=f'{member.mention}, this is your Ticket: {ticket_channel.mention}',
                    color=discord.Color.green(),
                    timestamp=datetime.now()
                )
                await interaction.response.send_message(embed=em1, ephemeral=True)

            except:
                em1E = discord.Embed(
                    title='📬 Error!',
                    description=f'{member.mention}, I had a issue while creating your Ticket, report this to the Owner/Founder asap !',
                    color=discord.Color.red(),
                    timestamp=datetime.now()
                )
                await interaction.response.send_message(embed=em1E, ephemeral=True)

            try:
                CloseButton = Button(label='Close Ticket', style=discord.ButtonStyle.red, custom_id='close')
                view = discord.ui.View(timeout=None)
                view.add_item(CloseButton)

                em2 = discord.Embed(
                    title=f'Welcome to your Ticket, {interaction.user.name}',
                    description='*To close the Ticket use the Button below. If its not working use `/close`*\n\n\n'
                                '**To begin please fill out theese questions.**\n'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n'
                                '**↬** Created by dbxFlame\n'
                                '**↬** Created by dbxFlame\n'
                                '**↬** No view'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬',
                    color=discord.Color.green(),
                    timestamp=datetime.now()
                )
                em22 = discord.Embed(
                    description="This is the second embed + view"
                )
                await ticket_channel.send(embed=em2)
                await ticket_channel.send(embed=em22, view=view)

                async def button_callback(interaction):

                    CloseTicket = discord.Embed(
                        title=f"dbxFlame open source / Ticket System",
                        description=f"Ticket get closed in 3 Second's!",
                        color=discord.Color.red()
                    )

                    await interaction.response.send_message(embed=CloseTicket)
                    await asyncio.sleep(3)
                    await interaction.channel.delete()

                    TicketClosed = discord.Embed(
                        title=f"dbxFlame open source / Ticket System",
                        description=f"{interaction.user.mention}, your Ticket on **{interaction.guild.name}** got closed!\n",
                        color=0xffffff,
                        timestamp=datetime.now()
                    )

                    TicketClosed.add_field(name="\nThis could be because:",
                                           value="**↬** You haven't replied in 24h\n**↬** You haven't supplied enough evidence\n\n**✺ If you still need help, please make a new Support ticket ✺**\n",
                                           inline=False)
                    TicketClosed.add_field(name="Ticket Owner", value=f"{interaction.user.mention}", inline=True)
                    TicketClosed.add_field(name="Ticket Name", value=f"{ticket_channel}", inline=True)
                    TicketClosed.set_footer(text=f"Created by dbxFlame")
                    await member.send(embed=TicketClosed)

                CloseButton.callback = button_callback
                return


            except:
                em2E = discord.Embed(
                    title='📬 Error!',
                    description=f'{member.mention}, I had a issue while creating your Ticket, report this to the Owner/Founder asap !',
                    color=discord.Color.red(),
                    timestamp=datetime.now()
                )
                await ticket_channel.send(embed=em2E)

        if '2' in interaction.data['values']:
            cat = client.get_channel(123456789)  # füge die Categorie ID ein, wo die Tickets erstellt werden sollen

            ticket_channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}',
                                                                         category=cat,
                                                                         topic=f'Ticket by {interaction.user} \nClient-ID: {interaction.user.id}')
            await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True,
                                                 view_channel=True)
            await ticket_channel.set_permissions(interaction.guild.default_role, view_channel=False)
            try:
                em1 = discord.Embed(
                    title='📬 Ticket open!',
                    description=f'{member.mention}, this is your Ticket: {ticket_channel.mention}',
                    color=discord.Color.green(),
                    timestamp=datetime.now()
                )
                await interaction.response.send_message(embed=em1, ephemeral=True)

            except:
                em1E = discord.Embed(
                    title='📬 Error!',
                    description=f'{member.mention}, I had a issue while creating your Ticket, report this to the Owner/Founder asap !',
                    color=discord.Color.red(),
                    timestamp=datetime.now()
                )
                await interaction.response.send_message(embed=em1E, ephemeral=True)

            try:
                CloseButton = Button(label='Close Ticket', style=discord.ButtonStyle.red, custom_id='close')
                view = discord.ui.View(timeout=None)
                view.add_item(CloseButton)

                em2 = discord.Embed(
                    title=f'Welcome to your Ticket, {interaction.user.name}',
                    description='*To close the Ticket use the Button below. If its not working use `/close`*\n\n\n'
                                '**To begin please fill out theese questions.**\n'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n'
                                '**↬** Created by dbxFlame\n'
                                '**↬** Created by dbxFlame\n'
                                '**↬** No view'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬',
                    color=discord.Color.green(),
                    timestamp=datetime.now()
                )
                em22 = discord.Embed(
                    description="This is the second embed + view"
                )
                await ticket_channel.send(embed=em2)
                await ticket_channel.send(embed=em22, view=view)

                async def button_callback(interaction):

                    CloseTicket = discord.Embed(
                        title=f"dbxFlame open source / Ticket System",
                        description=f"Ticket get closed in 3 Second's!",
                        color=discord.Color.red()
                    )

                    await interaction.response.send_message(embed=CloseTicket)
                    await asyncio.sleep(3)
                    await interaction.channel.delete()

                    TicketClosed = discord.Embed(
                        title=f"dbxFlame open source / Ticket System",
                        description=f"{interaction.user.mention}, your Ticket on **{interaction.guild.name}** got closed!\n",
                        color=0xffffff,
                        timestamp=datetime.now()
                    )

                    TicketClosed.add_field(name="\nThis could be because:",
                                           value="**↬** You haven't replied in 24h\n**↬** You haven't supplied enough evidence\n\n**✺ If you still need help, please make a new Support ticket ✺**\n",
                                           inline=False)
                    TicketClosed.add_field(name="Ticket Owner", value=f"{interaction.user.mention}", inline=True)
                    TicketClosed.add_field(name="Ticket Name", value=f"{ticket_channel}", inline=True)
                    TicketClosed.set_footer(text=f"Created by dbxFlame")
                    await member.send(embed=TicketClosed)

                CloseButton.callback = button_callback
                return


            except:
                em2E = discord.Embed(
                    title='📬 Error!',
                    description=f'{member.mention}, I had a issue while creating your Ticket, report this to the Owner/Founder asap !',
                    color=discord.Color.red(),
                    timestamp=datetime.now()
                )
                await ticket_channel.send(embed=em2E)

        if '3' in interaction.data['values']:
            cat = client.get_channel(123456789)  # füge die Categorie ID ein, wo die Tickets erstellt werden sollen

            ticket_channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}',
                                                                         category=cat,
                                                                         topic=f'Ticket by {interaction.user} \nClient-ID: {interaction.user.id}')
            await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True,
                                                 view_channel=True)
            await ticket_channel.set_permissions(interaction.guild.default_role, view_channel=False)
            try:
                em1 = discord.Embed(
                    title='📬 Ticket open!',
                    description=f'{member.mention}, this is your Ticket: {ticket_channel.mention}',
                    color=discord.Color.green(),
                    timestamp=datetime.now()
                )
                await interaction.response.send_message(embed=em1, ephemeral=True)

            except:
                em1E = discord.Embed(
                    title='📬 Error!',
                    description=f'{member.mention}, I had a issue while creating your Ticket, report this to the Owner/Founder asap !',
                    color=discord.Color.red(),
                    timestamp=datetime.now()
                )
                await interaction.response.send_message(embed=em1E, ephemeral=True)

            try:
                CloseButton = Button(label='Close Ticket', style=discord.ButtonStyle.red, custom_id='close')
                view = discord.ui.View(timeout=None)
                view.add_item(CloseButton)

                em2 = discord.Embed(
                    title=f'Welcome to your Ticket, {interaction.user.name}',
                    description='*To close the Ticket use the Button below. If its not working use `/close`*\n\n\n'
                                '**To begin please fill out theese questions.**\n'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n'
                                '**↬** Created by dbxFlame\n'
                                '**↬** Created by dbxFlame\n'
                                '**↬** No view'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬',
                    color=discord.Color.green(),
                    timestamp=datetime.now()
                )
                em22 = discord.Embed(
                    description="This is the second embed + view"
                )
                await ticket_channel.send(embed=em2)
                await ticket_channel.send(embed=em22, view=view)

                async def button_callback(interaction):

                    CloseTicket = discord.Embed(
                        title=f"dbxFlame open source / Ticket System",
                        description=f"Ticket get closed in 3 Second's!",
                        color=discord.Color.red()
                    )

                    await interaction.response.send_message(embed=CloseTicket)
                    await asyncio.sleep(3)
                    await interaction.channel.delete()

                    TicketClosed = discord.Embed(
                        title=f"dbxFlame open source / Ticket System",
                        description=f"{interaction.user.mention}, your Ticket on **{interaction.guild.name}** got closed!\n",
                        color=0xffffff,
                        timestamp=datetime.now()
                    )

                    TicketClosed.add_field(name="\nThis could be because:",
                                           value="**↬** You haven't replied in 24h\n**↬** You haven't supplied enough evidence\n\n**✺ If you still need help, please make a new Support ticket ✺**\n",
                                           inline=False)
                    TicketClosed.add_field(name="Ticket Owner", value=f"{interaction.user.mention}", inline=True)
                    TicketClosed.add_field(name="Ticket Name", value=f"{ticket_channel}", inline=True)
                    TicketClosed.set_footer(text=f"Created by dbxFlame")
                    await member.send(embed=TicketClosed)

                CloseButton.callback = button_callback
                return


            except:
                em2E = discord.Embed(
                    title='📬 Error!',
                    description=f'{member.mention}, I had a issue while creating your Ticket, report this to the Owner/Founder asap !',
                    color=discord.Color.red(),
                    timestamp=datetime.now()
                )
                await ticket_channel.send(embed=em2E)