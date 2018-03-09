import discord
from discord.ext import commands
import __main__ as neko
from random import choice, randint
import aiomysql
import asyncio
import time
from datetime import datetime


class Mycog():
    'My custom cog that does stuff!'

    def __init__(self, bot):
        self.bot = bot
        self.loop = asyncio.get_event_loop()
        self.footer = "Visit the NekoTony's Lounge | https://discord.gg/mBU7rSv"

    @commands.command()
    async def profile(self, ctx, user: discord.User=None):
        'BEL'
        if user is None:
            user = ctx.author
        guild = ctx.guild
        await neko.setup_profiles(user)
        embed = discord.Embed(title='{} Profile!! '.format(user.display_name), color=await self.color(user))
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='Relationship Status :heart_eyes: ', value=await self.married(user))
        embed.add_field(name='Wallet :dollar:', value=await self.dollars(user))
        embed.add_field(name='About Me :pen_ballpoint:', value=await self.about(user), inline=False)
        embed.add_field(name='Achievements :ribbon:', value=await self.achieve(user), inline=False)
        embed.add_field(name='Bot Staff Notes :notepad_spiral:', value=await self.notes(user), inline=False)
        embed.set_footer(text=self.footer)
        await ctx.send(embed=embed)

    @commands.command()
    async def marry(self, ctx, user: discord.User):
        'BEL'
        author = ctx.author
        guild = ctx.guild
        channel = ctx.channel
        await neko.setup_profiles(author)
        await neko.setup_profiles(user)
        compliments = ['hunk of chunk', 'fine thing', 'pure heart of twizzler', 'lifetime obsess', "christmas dancin' cowboy", 'not NekoTony',
                       'piece of ass cake', 'loveable rainbow', 'dank memer', 'soon to be star', 'Won "Must likely to divorice you" in high school.']
        await ctx.send("{}, do you take this **{}** to be your whatever, to be one, to be UGHHHH!! Do you just want to marry, **{}**? Yes or No? *I knew i shouldn't have got the ordained minister lincense.*".format(user.mention, choice(compliments), author.display_name))

        def check(m):
            return m.channel == channel and m.author == user
        response = await self.bot.wait_for('message')
        if response.content.lower() not in ['y', 'yes', 'sure', 'ok', 'fuck off', 'i do']:
            return await ctx.send("OOOOOOO, YOU'VE BEEEN REJECTED.")
        marry = await self.marrie(user, author)
        if marry == 2:
            await ctx.send("You can marry only up to 2 people. You should be happy we allowed you to have more than one. Are marriage laws haven't advance that far yet to allow 4 people marriages. :I")
        elif marry == 'ERR':
            await ctx.send('There was an error :O')
        elif marry == 'user':
            await ctx.send('**{}** is already married!'.format(user.display_name))
        elif marry == 'author':
            await ctx.send('**{}** is already married!'.format(author.display_name))
        elif marry == 'Eh2':
            await ctx.send("You can't marry the same person twice!")
        else:
            await ctx.send('You are now married to **{}**.'.format(marry))

    @commands.command()
    async def divorce(self, ctx, user: discord.User):
        'BEL'
        author = ctx.author
        guild = ctx.guild
        await neko.setup_profiles(author)
        await neko.setup_profiles(user)
        marry = await self.div(user, author)
        if marry == 'Single':
            await ctx.send("Oh you lucky bachelor. You're already single! Now go out and enjoy life....")
        elif marry == 'ERR':
            await ctx.send('There was an error :O')
        elif marry == 'No':
            await ctx.send("You can't divorice someone you haven't married, no matter how much you want he/she to pay for child support.")
        else:
            await ctx.send('You have now divoriced **{}**. Have fun with child support!'.format(marry.mention))

    @commands.command()
    async def setabout(self, ctx, *, about):
        'Set about, needs to be 500 characters.'
        author = ctx.author
        guild = ctx.guild
        await neko.setup_profiles(author)
        ok = await neko.set_field(author.id, 'about', about[:500], 'profiles', 'userid')
        if ok is 'GUD':
            return await ctx.send('Your about message has been set! It will only show the first 500 characters though.')
        await ctx.send('There was an error.')

    @commands.command()
    async def pickanum(self, ctx, num=None):
        'Unlock a random achievement'
        currnet = time.time()
        author = ctx.author
        guild = ctx.guild
        channel = ctx.channel
        await neko.setup_profiles(author)
        unlock = await neko.field(author.id, 'unlock_timestamp', 'profiles', 'userid')
        first = False
        if author.id not in [180339602798804992]:
            if len(unlock) == 0:
                first = True
            if first is False:
                old = datetime.fromtimestamp(
                    float(unlock)).strftime('%Y-%m-%d %H:%M:%S')
                old = datetime.strptime(old, '%Y-%m-%d %H:%M:%S')
                now = time.time()
                now = datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
                now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
                final = now - old
                print(final.days)
                if final.days < 1:
                    return await ctx.send('Sadly, you must wait a day before playing again. You have **{}** left.'.format(self.display_time(86400 - final.seconds)))
        if num is None:
            await ctx.send("Welcome to **Pick a Number**!! Here, you pick a number between `1-99` and if it's in our 20 randomly picked number, you could win a random profile. Make sure you only type a number and have fun! So sweet thang, what's your number!")

            def check(m):
                return m.channel == channel and m.author == author
            response = await self.bot.wait_for('message', check=check)
            currnet = time.time()
            try:
                num = int(response.content)
            except:
                return await ctx.send('Not a valid number, please try again.')
        else:
            try:
                num = int(num)
            except:
                return await ctx.send('Not a valid number, please try again.')
        num = str(num)
        if len(num) > 2:
            return await ctx.send('Number must be between `1-99`. Try again! :D')
        check = self.pickanum_check(num)
        if check[0] is True:
            await ctx.send('**Congrats. you have won! :confetti_ball:**\nHere were your lucky numbers for today: `{}`'.format(', '.join(check[1])))
            ok = choice(['achieve', 'coins', 'coins'])
            print(ok)
            await ctx.send('Picking prize, please wait!')
            await asyncio.sleep(5)
            if ok == 'coins':
                amount = randint(1, 20)
                dollars = await neko.field(author.id, 'dollars', 'profiles', 'userid')
                total = int(dollars) + amount
                ok = await neko.set_field(author.id, 'dollars', str(total), 'profiles', 'userid')
                return await ctx.send('You had earned ${0:,}! Have fun spending it!'.format(amount))
            elif ok == 'achieve':
                rewards = await neko.field(author.id, 'rewards', 'profiles', 'userid')
                rewards = eval(rewards)
                achieve = 'Has won the Pick-A-Num Game! Congrats!'
                if achieve in rewards:
                    achieve = 'Won this Pick-A-Num twice! Get a life! :grin:'
                    if achieve in rewards:
                        amount = randint(1, 20)
                        dollars = await neko.field(author.id, 'dollars', 'profiles', 'userid')
                        total = int(dollars) + amount
                        ok = await neko.set_field(author.id, 'dollars', str(total), 'profiles', 'userid')
                        return await ctx.send("You already won two badges from this game. I'll just give you ${0:,} money.".format(amount))
                rewards += ['{}'.format(achieve)]
                ok = await neko.set_field(author.id, 'rewards', rewards, 'profiles', 'userid')
                if ok is 'GUD':
                    return await ctx.send('Here, you have unlocked a new achievement: ```{}```'.format(achieve))
        else:
            await ctx.send('**Opps, try again tommorow... :frowning2: **\nHere were your lucky numbers for today: `{}`'.format(', '.join(check[1])))
        ok = await neko.set_field(author.id, 'unlock_timestamp', str(currnet), 'profiles', 'userid')
        if ok == 'ERR':
            return await ctx.send('There was an error.')

    @commands.command()
    async def beepadorp(self, ctx, channel: discord.TextChannel, *, msg):
        'Announce a message'
        author = ctx.author
        if author.id != 198948853611757568:
            return
        if ctx.guild == 274617826000502785:
            return
        await channel.send(msg)

    @commands.command()
    async def setcolor(self, ctx, color):
        'Set Color\n\n        Needs to be Html Color Codes (Ex, #FFFFFF, #A4A4A4)\n\n        Get some here http://html-color-codes.info/\n        '
        author = ctx.author
        guild = ctx.guild
        await neko.setup_profiles(author)
        color = color.replace('#', '')
        color = color.replace('0x', '')
        if len(color) != 6:
            return await ctx.send('Color needs to be an html color code. Check out some here:\n\nhttp://html-color-codes.info/')
        color = '0x{}'.format(color)
        ok = await neko.set_field(author.id, 'color', str(color), 'profiles', 'userid')
        if ok is 'GUD':
            return await ctx.send("You're profile color has been set to **{}**.".format(color.replace('0x', '#')))
        await ctx.send('There was an error')

    @commands.command()
    async def givecoins(self, ctx, amount, user: discord.User=None):
        'Give coins for owners only'
        author = ctx.author
        if user is None:
            user = author
        roles = [x.name.lower() for x in author.roles]
        if author.id != 180339602798804992:
            return await ctx.send('Only NekoTony, the lord and master, can do this command.')
        dollars = await neko.field(user.id, 'dollars', 'profiles', 'userid')
        total = int(dollars) + int(amount)
        ok = await neko.set_field(user.id, 'dollars', str(total), 'profiles', 'userid')
        return await ctx.send('**{}** earned ${0:,}! Have fun spending...'.format(user.display_name, int(amount)))

    @commands.command()
    async def leaderboard(self, ctx, amount=10):
        'View the richest users'
        ok = await self.board_stats(amount)
        top_users = []
        top_coins = []
        if amount > 20:
            return
        for x in ok:
            top_users.append(str(x[0]))
        for x in ok:
            top_coins.append(str(x[1]))
        embed = discord.Embed(title='Global Leader Boards | Dollars :dollar:')
        count = 0
        for x in top_users:
            user = discord.utils.get(self.bot.get_all_members(), id=x)
            if user is None:
                user = '???????'
            else:
                user = user.display_name
            embed.add_field(name='{}. {}'.format(
                count + 1, user), value='${0:,}'.format(int(top_coins[count])), inline=False)
            count += 1
            if count == int(amount):
                break
        amount = '{0:,}'.format(len(await self.board_stats(amount, False)))
        embed.set_footer(
            text='{} | {} users registered.'.format(self.footer, amount))
        await ctx.send(embed=embed)

    def rand_num(self):
        rand = []
        while True:
            num = randint(1, 99)
            if num in rand:
                continue
            rand.append(num)
            if len(rand) == 20:
                break
        return [str(x) for x in rand]

    def pickanum_check(self, num):
        randnums = self.rand_num()
        num = str(num)
        if num in randnums:
            return [True, randnums]
        else:
            return [False, randnums]

    async def on_message(self, message):
        m = message.content.lower()
        channel = message.channel
        author = message.author
        msg = message.content
        if author.bot:
            return
        if msg.lower() == 'tont monie':
            d = await self.dollars(author)
            await channel.send('Bitch, you got dough. The certain amount, idk. I think it is `{}`. Nice!!'.format(d))
        if msg.lower() == 'tont hun':
            d = await self.married(author, True)
            await channel.send('OMG! OMG! OMG! GOOOOSSSSSIIIIIPPP!!! Yooou, i mean you, is married to **{}**? Boi, this is sooo going on my blog.'.format(d))

    async def married(self, user, t=False):
        married = await neko.field(user.id, 'marryid', 'profiles', 'userid')
        married = eval(married)
        if len(married) <= 0:
            return 'Living the single life.'
        else:
            inlove = []
            for id in married:
                person = discord.utils.get(self.bot.get_all_members(), id=id)
                inlove.append(str(person.display_name.title()))
            if len(inlove) == 2:
                married = '{} | {}'.format(inlove[0], inlove[1])
            else:
                married = inlove[0]
            if t is True:
                return married
            return 'Married to **{}**.'.format(married)

    async def notes(self, user):
        notes = await neko.field(user.id, 'notes', 'profiles', 'userid')
        if notes == 'NONE':
            return 'Currently no notes by Bot Staff.'
        else:
            return notes

    async def marrie(self, user, author):
        married = await neko.field(user.id, 'marryid', 'profiles', 'userid')
        married = eval(married)
        marrieda = await neko.field(author.id, 'marryid', 'profiles', 'userid')
        marrieda = eval(marrieda)
        oh = await self.ehhh()
        if user.id in oh:
            return 'user'
        if author.id in oh:
            return 'author'
        if id in married:
            return 'Eh'
        if id in marrieda:
            return 'Eh'
        married += ['{}'.format(author.id)]
        ok = await neko.set_field(user.id, 'marryid', married, 'profiles', 'userid')
        if ok != 'GUD':
            return 'ERR'
        marrieda += ['{}'.format(user.id)]
        ok = await neko.set_field(author.id, 'marryid', marrieda, 'profiles', 'userid')
        if ok != 'GUD':
            return 'ERR'
        return discord.utils.get(self.bot.get_all_members(), id=user.id)

    async def div(self, user, author):
        married = await neko.field(user.id, 'marryid', 'profiles', 'userid')
        married = eval(married)
        marrieda = await neko.field(author.id, 'marryid', 'profiles', 'userid')
        marrieda = eval(marrieda)
        if len(married) == 0:
            return 'Single'
        if user.id not in marrieda:
            return 'No'
        if author.id not in married:
            return 'No'
        married = [x for x in married if x != author.id]
        ok = await neko.set_field(user.id, 'marryid', married, 'profiles', 'userid')
        if ok != 'GUD':
            return 'ERR'
        marrieda = [x for x in marrieda if x != user.id]
        ok = await neko.set_field(author.id, 'marryid', married, 'profiles', 'userid')
        if ok != 'GUD':
            return 'ERR'
        return discord.utils.get(self.bot.get_all_members(), id=user.id)

    async def dollars(self, user):
        dollars = await neko.field(user.id, 'dollars', 'profiles', 'userid')
        return '${0:,}'.format(int(dollars))

    async def about(self, user):
        about = await neko.field(user.id, 'about', 'profiles', 'userid')
        if about == 'NONE':
            return "There's nothing to see!"
        return about

    def display_time(self, seconds, granularity=2):
        intervals = (('dys', 86400), ('hrs', 3600), ('mins', 60), ('secs', 1))
        result = []
        for (name, count) in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append('{}{}'.format(value, name))
        return ', '.join(result[:granularity])

    async def achieve(self, user):
        rewards = await neko.field(user.id, 'rewards', 'profiles', 'userid')
        rewards = eval(rewards)
        if len(rewards) <= 0:
            return 'Currently have not achieved anything!'
        reward = []
        count = 1
        for x in rewards:
            eh = '{}. {}'.format(count, x)
            count += 1
            reward.append(eh)
        rewards = '\n'.join(reward)
        return rewards

    async def color(self, user):
        color = await neko.field(user.id, 'color', 'profiles', 'userid')
        return int(color, 16)

    async def ehhh(self):
        conn = await aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='smashbot1567', db='neko', autocommit=True, loop=self.loop)
        async with conn.cursor() as cur:
            check = 'SELECT marryid FROM profiles'
            check = await cur.execute(check)
            resz = []
            for res in await cur.fetchall():
                res = eval(res[0])
                for id in res:
                    resz.append(id)
            return list(set(resz))

    async def board_stats(self, amount, amt=True):
        conn = await aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='smashbot1567', db='neko', autocommit=True, loop=self.loop)
        async with conn.cursor() as cur:
            check = 'SELECT dollars, userid FROM profiles ORDER BY dollars'
            check = await cur.execute(check)
            resz = {

            }
            for res in await cur.fetchall():
                resz[neko.decode(res[1])] = int(res[0])
            resz = sorted(resz.items(), key=(lambda x: x[1]), reverse=True)
            count = 0
            final = resz
            if amt is True:
                final = []
                for x in resz:
                    final.append(x)
                    count += 1
                    if count == int(amount):
                        break
            return final


def setup(bot):
    bot.add_cog(Mycog(bot))
