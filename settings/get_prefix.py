import json
import discord
from discord.ext import commands
from settings.config import settings

bot = commands.Bot(command_prefix=settings['prefix'], intents=discord.Intents.all())

curr_dir = (os.path.abspath(os.curdir))
project_dir = os.path.dirname(abs_path)
prefix_dir = project_dir + '\settings\prefix.json'


@bot.event
async def on_guild_join(guild):
    with open('C:/Users/Andrew/PycharmProjects/seren/settings/prefix.json', 'r') as f:
        prefix = json.load(f)
    prefix[str(guild.id)] = '-'
    with open('C:/Users/Andrew/PycharmProjects/seren/settings/prefix.json', 'w') as w:
        json.dump(prefix, w, indent=4)


bot.run(settings['token'])
