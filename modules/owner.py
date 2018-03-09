import discord
from discord.ext import commands
import aiohttp
import base64
import importlib
import __main__ as neko
import asyncio
import time
import datetime


class Owners():
    'Bot Owners Only'

    def __init__(self, bot):
        self.bot = bot
        self.owner = 180339602798804992

    @commands.command()
    async def upava(self, ctx):
        'Unload a Module'
        if ctx.author.id != self.owner:
            return
        with open('rawr.png', 'rb') as f:
            icon = f.read()
        await self.bot.edit_profile(None, avatar=icon)

    @commands.command()
    async def unload(self, ctx, module: str):
        'Unload a Module'
        if ctx.author.id != self.owner:
            return
        filename = module
        module = 'modules.{}'.format(module)

        try:
            self.bot.unload_extension(module)
            await ctx.send('Unloaded {}.py.'.format(filename))
        except:
            return await ctx.send('Failed to unload')
    
    @commands.command()
    async def announce(self, ctx, *, text):
        author = ctx.author
        if author.id not in [180339602798804992, 279810398264360962, 281584044972441600]:
            return
        time = datetime.datetime.now().strftime("%A, %m/%d/%y @%I:%M%p")
        guild = self.bot.get_guild(274617826000502785)
        channel = guild.get_channel(274618562151317506)
        msg = ":exclamation: **Announcement at {}**\n".format(time)
        msg += text
        msg += "\n\n*~{}*\n\n**Make sure to voice your opinion with reactions. <:nekolove:388501088099368962>**".format(author.name.title())
        await channel.send(msg)

    @commands.command()
    async def load(self, ctx, module: str):
        'Load a Module'
        if ctx.author.id != self.owner:
            return
        filename = module
        module = 'modules.{}'.format(module)
        try:
            mod_obj = importlib.import_module(module)
            importlib.reload(mod_obj)
            self.bot.load_extension(mod_obj.__name__)
            await ctx.send('Loaded {}.py.'.format(filename))
        except (AttributeError, ImportError) as e:
            return await ctx.send('```py\n{}: {}\n```'.format(type(e).__name__, str(e)))

    @commands.command()
    async def reload(self, ctx, module: str):
        'reload a Module'
        if ctx.author.id != self.owner:
            return
        filename = module
        module = 'modules.{}'.format(module)
        if ctx.author.id != self.owner:
            return
        try:
            self.bot.unload_extension(module)
            mod_obj = importlib.import_module(module)
            importlib.reload(mod_obj)
            self.bot.load_extension(mod_obj.__name__)
            await ctx.send('Reloaded {}.py.'.format(filename))
        except (AttributeError, ImportError) as e:
            return await ctx.send('```py\n{}: {}\n```'.format(type(e).__name__, str(e)))

    @commands.command()
    async def ping(self, ctx):
        'Ping Pong'
        await ctx.send('Pong!')

    @commands.command(hidden=True)
    async def eval(self, ctx, *, code):
        'Evaluates code'
        if ctx.author.id != self.owner:
            return

        def check(m):
            if m.content.strip().lower() == 'more':
                return True
        author = ctx.author
        channel = ctx.channel
        code = code.strip('` ')
        result = None
        global_vars = globals().copy()
        global_vars['bot'] = self.bot
        global_vars['ctx'] = ctx
        global_vars['message'] = ctx.message
        global_vars['author'] = ctx.author
        global_vars['channel'] = ctx.channel
        global_vars['server'] = ctx.guild
        try:
            result = eval(code, global_vars, locals())
        except Exception as e:
            if channel.is_private:
                color = 16777215
            else:
                color = author.color
            result = '{}: {}'.format(type(e).__name__, str(e))
            embed = discord.Embed(
                colour=color, description='{}'.format(result))
            embed.set_author(name='Eval', icon_url=author.avatar_url)
            await channel.send(embed=embed)
            return
        if asyncio.iscoroutine(result):
            result = await result
        result = str(result)
        print(result)
        if channel.is_private:
            color = 16777215
        else:
            color = author.color
        embed = discord.Embed(colour=color, description='{}'.format(result))
        embed.set_author(name='Eval', icon_url=author.avatar_url)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Owners(bot))
