import json
import discord
from discord.ext import commands
from settings.config import settings
import os

bot = commands.Bot(command_prefix=settings['prefix'], intents=discord.Intents.all())
bot.remove_command('help')

curr_dir = (os.path.abspath(os.curdir))
project_dir = os.path.dirname(curr_dir)
prefix_dir = project_dir + '\settings\prefix.json'


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if interaction:
        return
    if error:
        return


@bot.event
async def on_guild_join(guild):
    with open(prefix_dir, 'r') as f:
        prefix = json.load(f)
    prefix[str(guild.id)] = '-'
    with open(prefix_dir, 'w') as w:
        json.dump(prefix, w, indent=4)


bot.run(settings['token'])
