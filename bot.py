import asyncio
import datetime

from urllib3 import PoolManager
from urllib3.exceptions import HTTPError

from discord.ext import commands

from importlib import import_module

bot = commands.Bot(command_prefix='p!', description='Kirito\'s general purpose bot')

@bot.event
async def on_ready():
    pass

@bot.command()
async def ping():
    await bot.say(':carrot:')

@bot.command()
async def uptime():
    pass

def is_su(ctx):
    print(ctx.message.author.id)
    return ctx.message.author.id in ["267445257321316363","343932489401892864"]

@bot.group(pass_context=True)
@commands.check(is_su)
async def sudo(ctx, cmd : str):
    eval(cmd)
    await bot.whisper("Command %r successfully executed." % cmd)

@bot.command()
async def math(formula : str):
    await bot.say('not yet implemented')

@bot.command()
async def isup(domain : str):
    global pool
    try:
        r = pool.request('GET', domain)
        if r.status == 200:
            await bot.say('%s is up!' % domain)
        else:
            await bot.say('Response code %d.' % r.status)
    except (ConnectionError, HTTPError) as e:
        await bot.say(e)


token = None

with open('token.txt') as f:
    token = f.read().strip()

pool = PoolManager(100)

bot.run(token)
