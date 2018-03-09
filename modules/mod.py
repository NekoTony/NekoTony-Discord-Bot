
import discord
from discord.ext import commands
from random import choice
import __main__ as neko
import ast
import time


class Mod():
    'Mod Rep'

    def __init__(self, bot):
        self.bot = bot
        self.ids = []

    @commands.command()
    async def setlog(self, ctx, channel: discord.TextChannel):
        'Set Log Channel'
        guild = ctx.guild
        await neko.setup_guilds(guild)
        if ctx.author.id != guild.owner.id:
            return
        if channel is None:
            channel = ctx.channel
        ok = await neko.set_field(guild.id, 'channelid', channel.id, 'servers', 'serverid')
        await ctx.send(str(ok))

    @commands.command()
    async def warn(self, ctx, points, user: discord.User):
        'Warn a user'
        guild = ctx.guild
        author = ctx.author
        await neko.setup_guilds(guild)
        roles = [x.id for x in author.roles]
        guildrole = await neko.field(guild.id, 'roleid', 'servers', 'serverid')
        if user.id == author.id:
            return await ctx.send("Can't warn youself")
        if guildrole == 'NONE':
            return await ctx.send('Please set staff role with n@setmodrole.')
        if guildrole not in roles:
            return
        if user.bot is True:
            return await ctx.send("Can't warn a bot, sorry.")
        if (points is None) or (user is None):
            return await ctx.send('Please used the proper command: n@warn [amount of points] [user]')
        ok = await neko.setup_warnings(guild, user)
        if ok == 'ERR':
            return await ctx.send('There was an error.')
        oldpoints = await neko.field(user.id, 'points', 'warnings', 'userid')
        await neko.set_field(user.id, 'points', str(int(oldpoints) + int(points)), 'warnings', 'userid')
        maxpoints = await neko.field(guild.id, 'max_points', 'servers', 'serverid')
        msg = "{}, have been warned with {} and currently have {} points. If you reach {} points, you'll be banned from **{}**. Thank you!".format(
            user.mention, points, str(int(oldpoints) + int(points)), maxpoints, guild)
        await ctx.send(msg)
        points = await neko.field(user.id, 'points', 'warnings', 'userid')
        if int(points) >= int(maxpoints):
            field = 'ban'
            await user.ban()
        else:
            field = 'warning'
        reason = await self.reason(author, ctx.channel, guild)
        if reason is None:
            return await ctx.send('Please set staff role with n@setlog.')
        if field == 'ban':
            reason = '{} | Was banned for having over {} points with {} points'.format(
                reason, points, maxpoints)
        await self.log(user, author, guild, field, reason)

    @commands.command()
    async def ban(self, ctx, user: discord.User):
        'Ban a user'
        guild = ctx.guild
        author = ctx.author
        await neko.setup_guilds(guild)
        roles = [x.id for x in author.roles]
        guildrole = await neko.field(guild.id, 'roleid', 'servers', 'serverid')
        if user.id == author.id:
            return await ctx.send("Can't ban youself")
        if guildrole == 'NONE':
            return await ctx.send('Please set staff role with n@setmodrole.')
        if guildrole not in roles:
            return
        await user.ban()
        reason = await self.reason(author, ctx.channel, guild)
        if reason is None:
            return await ctx.send('Please set staff role with n@setlog.')
        await self.log(user, author, guild, 'ban', reason)

    @commands.command()
    async def kick(self, ctx, user: discord.User):
        'Kick a person'
        guild = ctx.guild
        author = ctx.author
        await neko.setup_guilds(guild)
        roles = [x.id for x in author.roles]
        guildrole = await neko.field(guild.id, 'roleid', 'servers', 'serverid')
        if user.id == author.id:
            return await ctx.send("Can't kick youself")
        if guildrole == 'NONE':
            return await ctx.send('Please set staff role with n@setmodrole.')
        if guildrole not in roles:
            return
        await user.kick()
        reason = await self.reason(author, ctx.channel, guild)
        if reason is None:
            return await ctx.send('Please set staff role with n@setlog.')
        await self.log(user, author, guild, 'kick', reason)

    @commands.command()
    async def setmodrole(self, ctx, role: discord.Role):
        'Set Mod Role'
        guild = ctx.guild
        author = ctx.author
        await neko.setup_guilds(guild)
        print(role)
        if author.id != 180339602798804992:
            if author.id != guild.owner.id:
                return
        if role is None:
            return await ctx.send('Need to provide a role. n@setmodrole [role]')
        ok = await neko.set_field(guild.id, 'roleid', role.id, 'servers', 'serverid')
        if ok == 'GUD':
            await ctx.send('Has set mod commands to people with role **{}**'.format(role))

    @commands.command()
    async def maxpoints(self, ctx, points):
        'Set for Max Points'
        guild = ctx.guild
        author = ctx.author
        await neko.setup_guilds(guild)
        if points is None:
            return await ctx.send('Use this command: n@maxpoints [points]')
        if author.id != guild.owner.id:
            return
        ok = await neko.set_field(guild.id, 'max_points', points, 'servers', 'serverid')
        if ok == 'GUD':
            await ctx.send('Set max points for warnings to **{}**. If someone goes higher then the max points, they will be banned.'.format(points))

    @commands.command()
    async def pingmods(self, ctx, *, reason):
        'Ping Mods'
        guild = ctx.guild
        author = ctx.author
        await neko.setup_guilds(guild)
        roleid = await neko.field(guild.id, 'roleid', 'servers', 'serverid')
        if roleid == 'NONE':
            return await ctx.send('Owner needs to set mod role with `s#setmodrole`.')
        mods = [y for y in guild.members if str(
            roleid) in [x.id for x in y.roles]]
        mods = [y.id for y in mods if str(y.status) != 'offline']
        await ctx.send('<@{}>, you have been pinged. Reason:\n**{}**'.format(choice(mods), reason))

    @commands.command()
    async def ahs(self, ctx, type, *, role):
        'AHS Flairs'
        guild = ctx.guild
        author = ctx.author
        channel = ctx.channel
        channelid = 241250050536112128
        if type.lower() not in ['add', 'remove']:
            return await ctx.send("You're role type must `remove` or `add`.")
        if guild.id != 241243173148557312:
            return await ctx.send('Ya need to be in the official server!')
        if channel.id != channelid:
            return await ctx.send('Please flair in <#{}>. Thank you.'.format(channelid))
        guildroles = [x for x in guild.roles if x.name.lower() not in [
            'moderators', 'server owner', "server's bot", 'dsl', "nekotony's assitant", '@everyone']]
        guildroles = [x.name.lower() for x in guildroles]
        role = discord.utils.get(guild.roles, name=role.title())
        if role.name.lower() not in guildroles:
            return await ctx.send("Sorry, that role doesn't exist")
        try:
            await author.add_roles(role)
        except:
            return ctx.send('Error adding role!')
        await ctx.send('**{}** has been {}ed to your profile.'.format(role.name.title(), type))

    async def on_message(self, message):
        channel = message.channel
        author = message.author
        if channel.id != 378326789916852224:
            return
        if author.bot:
            return
        if author.id in self.ids:
            return await message.delete()

        def check(m):
            return m.channel == channel and m.author == author
        if message.content.lower() != 'i, sign up for secret santa 2017 and promise to provide and receive gifts for this event.':
            return await message.delete()
        msg = await message.channel.send('{}, What do you want for secret santa?'.format(message.author.mention))
        r = await self.bot.wait_for('message', timeout=300, check=check)
        if r is None:
            await msg.delete()
            return
        self.ids.append(message.author.id)
        await msg.delete()
        try:
            await r.delete()
        except:
            pass
        tim = str(time.strftime('%A %B %d, %Y at %I:%M%p'))
        msg = "{} has signed up for **Secret Santa 2017**. We'll assign you to a user on November 25th.\n\nI want: ```{}```User ID: **{}**\nJoin Date: **{}**\nUsers signed up: **{}**\nId's for users signed up: ```{}```".format(
            message.author.mention, r.content, message.author.id, tim, len(self.ids), ', '.join(self.ids))
        await message.channel.send(msg)
        await message.delete()

    async def reason(self, author, channel, guild):
        await neko.setup_guilds(guild)
        logchannel = await neko.field(guild.id, 'channelid', 'servers', 'serverid')
        if logchannel == 'NONE':
            return None
        await ctx.send('Current sending log to log channel. Would you like to add a reason, {}? `Y/n`'.format(author.mention))
        reason = 'Not Provided'

        def check(m):
            return m.channel == channel and m.author == author
        responce = await self.bot.wait_for('message', check=check)
        if responce.content.lower() in ['y', 'yes', 'sure', 'ok']:
            await ctx.send('Ok, what is the reason behind the warning?')
            responce = await self.bot.wait_for('message', check=check)
            reason = responce.content
        return reason

    async def log(self, user, author, guild, field, reason):
        logchannel = await neko.field(guild.id, 'channelid', 'servers', 'serverid')
        channel = guild.get_channel(logchannel)
        if field.lower() == 'warning':
            color = 16777215
            embed = discord.Embed(
                title='{} has been warned.'.format(user), color=color)
            embed.add_field(name='{} current points:'.format(user), value='{}'.format(await neko.field(user.id, 'points', 'warnings', 'userid')))
            embed.add_field(name='Warned by:', value=author)
            embed.add_field(name='Reason for warning:', value=reason)
            embed.add_field(name='Current Server:', value=guild)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.set_footer(text="If you reach {}, you'll be automaticly banned. If you're the owner, you can change the max points set with s@maxpoints".format(await neko.field(guild.id, 'max_points', 'servers', 'serverid')))
            await channel.send(embed=embed)
        elif field.lower() == 'kick':
            color = 16777215
            embed = discord.Embed(
                title='{} has been kicked.'.format(user), color=color)
            embed.add_field(name='Kicked by:', value=author)
            embed.add_field(name='Reason for kicked:', value=reason)
            embed.add_field(name='Current Server:', value=guild)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            await channel.send(embed=embed)
        elif field.lower() == 'ban':
            color = 16777215
            embed = discord.Embed(
                title='{} has been banned.'.format(user), color=color)
            embed.add_field(name='Banned by:', value=author)
            embed.add_field(name='Reason for banned:', value=reason)
            embed.add_field(name='Current Server:', value=guild)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Mod(bot))
