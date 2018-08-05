import asyncio
import datetime

import yaml

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
    global sudoers
    return ctx.message.author.id in sudoers

@bot.group(pass_context=True)
@commands.check(is_su)
async def sudo(ctx, cmd : str):
    try:
        eval(cmd)
        await bot.whisper("Command %r successfully executed." % cmd)
    except Exception as e:
        await bot.whisper('Encountered error while executing %s!\n%s' % (cmd, e))

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

def main():
    global bot, pool, sudoers
    pool = PoolManager(100)

    token = None

    with open('config.yml') as f:
        config = yaml.load(f.read())
        token = config['token']
        sudoers = config['sudoers']

    bot.run(token)

if __name__ == '__main__':
    main()
