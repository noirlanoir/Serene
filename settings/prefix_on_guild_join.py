import json
import discord
from discord.ext import commands
from settings.config import settings

bot = commands.Bot(command_prefix=settings['prefix'], intents=discord.Intents.all())

curr_dir = (os.path.abspath(os.curdir))
project_dir = os.path.dirname(curr_dir)
prefix_dir = project_dir + '\settings\prefix.json'


@bot.event
async def on_guild_join(guild):
    with open(prefix_dir, 'r') as f:
        prefix = json.load(f)
    prefix[str(guild.id)] = '-'
    with open(prefix_dir, 'w') as w:
        json.dump(prefix, w, indent=4)


bot.run(settings['token'])
