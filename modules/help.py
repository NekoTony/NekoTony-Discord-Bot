import discord
from discord.ext import commands
import asyncio
from random import choice
import __main__ as neko
import aiohttp
from urllib.parse import urlparse
from os.path import splitext, basename


class Help():
    'Help Module by NekoTony'

    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @commands.command()
    async def help(self, ctx):
        'Help Command'
        author = ctx.author
        profile = 'Profile Commands'
        msg = "**NekoTony's Assitant** - Bot made for Nekotony#0047 use but anyone can enjoy.\n\n\n"
        msg += '```'
        with open('help.txt', 'r') as w:
            ok = w.read()
        msg += ok
        msg += '```\n\n'
        msg += '**TOS** By agreeing to use this bot, you allow us to gather server info for mod commands and such.'
        msg += '\n\nOfficial Server: https://discord.gg/mBU7rSv\nPatreon:  https://www.patreon.com/nekotony'
        try:
            await author.send(msg)
        except:
            await ctx.send(msg)

    async def on_member_join(self, member):
        guild = member.guild
        lounge = guild.get_channel(274618797510361091)
        wel = guild.get_channel(274617826000502785)
        if guild.id == 274617826000502785:
            role = discord.utils.get(guild.roles, id=275327496948285440)
            await member.add_roles(role)
            msg = "Welcome to **{}**, {}. Please read {} before posting! Thanks! :kiss:".format(guild.name.title(), member.mention, wel.mention)
            await lounge.send(msg)
    
    @commands.command()
    async def qotd(self, ctx, *, answer):
        author = ctx.author
        guild = ctx.guild
        if guild.id == 274617826000502785:
            official = self.bot.get_guild(274617826000502785)
            channel = discord.utils.get(official.channels, name='qotd')
            message = '**{}:** {}'.format(author, answer)
            await channel.send(message)
            await ctx.send('Your answer has been submitted to {}.'.format(channel.mention))

    async def on_member_remove(self, member):
        guild = member.guild
        channel = guild.get_channel(274618797510361091)
        if guild.id == 274617826000502785:
            msg = "Fine then, leave me **{}**. I'll be...ok.... :cry:".format(member.name.title())
            eee = await channel.send(msg)

    async def on_member_update(self, before, after):
        if before.id != 180339602798804992:
            return
        if before.avatar_url == after.avatar_url:
            return
        icon = await self.image_btye(after.avatar_url)
        guild = self.bot.get_guild(274617826000502785)
        await guild.edit(icon=icon)
        try:
            await self.bot.user.edit(avatar=icon)
        except:
            pass

    async def image_btye(self, url):
        url = url.replace('webp', 'png')
        async with aiohttp.ClientSession() as ses, ses.get(url) as r:
            ava = await r.read()
        with open('rawr.png', 'wb') as f:
            f.write(ava)
        with open('rawr.png', 'rb') as f:
            ava = f.read()
        return ava


def setup(bot):
    bot.add_cog(Help(bot))
