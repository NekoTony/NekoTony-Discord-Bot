import discord
from discord.ext import commands
import asyncio
import logging
import json
import aiohttp
import kyoukai
import werkzeug
import base64
import sys
import aiomysql
import traceback
import time
import string
import codecs

session = aiohttp.ClientSession()
loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)
app = kyoukai.Kyoukai('UserInfo', loop=loop)
description = "NekoTony's Assitant - Bot made for Nekotony use but everyone can enjoy."
startup_extensions = ['modules.owner',
                      'modules.help', 'modules.mod', 'modules.profile']
bot = commands.Bot(
    command_prefix=['n@', 'n!', 'n?', 'n#'], description=description)

@bot.event
async def on_command_error(ctx, error):
    channel = ctx.channel
    guild = ctx.guild
    author = ctx.author
    owner = discord.utils.get(ctx.bot.get_all_members(), id=180339602798804992)
    oguild = ctx.bot.get_guild(274617826000502785)
    ochannel = oguild.get_channel(344609238447816707)
    if isinstance(error, commands.MissingRequiredArgument):
        await send_cmd_help(ctx)
    elif isinstance(error, commands.BadArgument):
        await send_cmd_help(ctx)
    elif isinstance(error, commands.DisabledCommand):
        await channel.send('That command is disabled.')
    elif isinstance(error, commands.CommandInvokeError):
        if isinstance(channel, discord.abc.PrivateChannel):
            oneliner = 'You got an in DM **{}** ({}) caused by **{}** ({})\n'.format(
                channel, channel.id, author, author.id)
        else:
            oneliner = 'You got an error from server **{}** ({}) in channel **{}** ({}) caused by **{}** ({})\n'.format(
                guild, guild.id, channel, channel.id, author, author.id)
        traceback.print_tb(error.original.__traceback__)
        line = exc_traceback.tb_lineno
        oneliner += "```Error in command '{}' - {}: {}```".format(
            ctx.command.qualified_name, type(error.original).__name__, str(error.original))
        content = base64.urlsafe_b64encode(bytes(oneliner, 'utf-8'))
        await ochannel.send(oneliner)
        await channel.send('There seems to be some an error. We have sent a copy of the transcript to the owner. Please go to our bug channel in our community server and paste the following code: (link is https://discord.gg/mBU7rSv)')
        await channel.send(oneliner)
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.CheckFailure):
        pass
    elif isinstance(error, commands.NoPrivateMessage):
        await channel.send("Sorry bud, you can't use this command in Direct Message.")
    else:
        print(type(error).__name__, exc_info=error)
    return bot

@bot.event
async def on_ready():
    print('We are up!')
    await update_status()
    await update('https://bots.discord.pw/api')


@bot.event
async def on_guild_join(guild):
    await update('https://bots.discord.pw/api')
    await update_status()


@bot.event
async def on_guild_remove(guild):
    await update('https://bots.discord.pw/api')
    await update_status()


async def update_status():
    message = 'Profiles are here [n@help] | {} servers.'.format(
        len(bot.guilds))
    game = discord.Game(name=message, type=0)
    print(game)
    await bot.change_presence(game=game)


async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        commands = bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        for x in commands:
            await ctx.channel.send(x)
    else:
        commands = bot.formatter.format_help_for(ctx, ctx.command)
        for x in commands:
            await ctx.channel.send(x)


async def update(link):
    payload = json.dumps({
        'server_count': len(bot.guilds),
    })
    if link.lower() == 'https://bots.discord.pw/api':
        headers = {
            'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiIxODAzMzk2MDI3OTg4MDQ5OTIiLCJyYW5kIjo0OCwiaWF0IjoxNTAzMTExMTk3fQ.BNV3W8fY-k9F9mgS_Nv5JIS_TIEDejHm72B4mes7hrc',
            'content-type': 'application/json',
        }
    else:
        headers = {
            'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjE4MDMzOTYwMjc5ODgwNDk5MiIsImlhdCI6MTQ5Mzc2NTkyMn0.qJ7xfV31SKmt-m3re6tP-w8grGSBftjC00G5LAF-g28',
            'content-type': 'application/json',
        }
    url = '{0}/bots/{1.user.id}/stats'.format(link, bot)
    async with session.post(url, data=payload, headers=headers) as resp:
        print('{2} statistics returned {0.status} for {1}'.format(
            resp, payload, link))


async def setup_guilds(guild):
    conn = await aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='password', db='database', autocommit=True, loop=loop)
    async with conn.cursor() as cur:
        check = await cur.execute("SELECT serverid FROM servers WHERE serverid='{}'".format(encode(guild.id)))
        if check == 1:
            return 'ALR'
        reg_date = time.strftime('%B %d, %Y at %I:%M%p %Z')
        test = await cur.execute('INSERT INTO servers (serverid, max_points, servername, status, date, channelid, roleid)values (%s,%s,%s,%s,%s,%s,%s)', (encode(guild.id), '15', encode(guild.name.title()), 'ON', str(reg_date), 'NONE', 'NONE'))
    if test == 1:
        return 'GUD'
    else:
        return 'ERR'


async def setup_profiles(user):
    conn = await aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='password', db='database', autocommit=True, loop=loop)
    async with conn.cursor() as cur:
        check = await cur.execute("SELECT userid FROM profiles WHERE userid='{}'".format(encode(user.id)))
        if check == 1:
            return 'ALR'
        reg_date = time.strftime('%B %d, %Y at %I:%M%p %Z')
        test = await cur.execute('INSERT INTO profiles (userid, reg_date, about, marryid, rewards, dollars, notes, color)values (%s,%s,%s,%s,%s,%s,%s,%s)', (encode(user.id), str(reg_date), encode('NONE'), '[]', '[]', '000', encode('NONE'), '0xA4A4A4'))
    if test == 1:
        return 'GUD'
    else:
        return 'ERR'


async def setup_warnings(guild, user):
    conn = await aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='password', db='database', autocommit=True, loop=loop)
    async with conn.cursor() as cur:
        check = await cur.execute("SELECT serverid FROM warnings WHERE serverid='{}'".format(encode(guild.id)))
        if check == 1:
            check = await cur.execute("SELECT userid FROM warnings WHERE userid='{}'".format(encode(user.id)))
            if check == 1:
                return 'ALR'
        test = await cur.execute('INSERT INTO warnings (userid, username, serverid, servername, points)values (%s,%s,%s,%s,%s)', (encode('{}'.format(user.id)), encode('{}'.format(user.name)), encode('{}'.format(guild.id)), encode('{}'.format(guild.name)), '0'))
    if test == 1:
        return 'GUD'
    else:
        return 'ERR'


async def set_field(id, field, sett, db, o):
    id = str(encode('{}'.format(id)))
    if field not in ['max_points', 'points', 'status', 'marryid', 'rewards', 'dollars', 'color', 'unlock_timestamp']:
        sett = str(encode('{}'.format(sett)))
    conn = await aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='password', db='database', autocommit=True, loop=loop)
    async with conn.cursor() as cur:
        if field in ['rewards', 'marryid']:
            sett = '[{}]'.format(
                ', '.join((('"' + item) + '"' for item in sett)))
        query = await cur.execute("UPDATE {} SET {}='{}' WHERE {}='{}'".format(str(db.lower()), str(field.lower()), str(sett), str(o), str(id)))
    if query == 1:
        return 'GUD'
    else:
        return 'ERR'


async def field(char, field, db, o):
    field = field.lower()
    char = str(encode(char))
    conn = await aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='password', db='database', autocommit=True, loop=loop)
    async with conn.cursor() as cur:
        check = "SELECT {} FROM {} WHERE {}='{}'".format(
            str(field), str(db), str(o), str(char))
        check = await cur.execute(check)
        res = await cur.fetchone()
        oh = res[0]
        if field not in ['max_points', 'points', 'status', 'rewards', 'dollars', 'color', 'marryid', 'unlock_timestamp']:
            if oh == 'NONE':
                return str(oh)
            oh = decode(oh)
        return str(oh)


def encode(ok):
    ok = str(ok)
    ok = codecs.encode(ok.encode(), 'base64')
    ok = ok.decode().replace('\n', '')
    return ok


def decode(str):
    ok = codecs.decode(str.encode(), 'base64')
    return ok.decode()


if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            print('loaded {}.py'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
try:
    bot.run('')
except:
    print('Error running bot.')
