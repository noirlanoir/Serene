import json
import discord
from discord.ext import commands
from settings.config import settings
import os
import pymongo
from pymongo import MongoClient

bot = commands.Bot(command_prefix=settings['prefix'], intents=discord.Intents.all())
bot.remove_command('help')

curr_dir = (os.path.abspath(os.curdir))
project_dir = os.path.dirname(curr_dir)
prefix_dir = project_dir + '\settings\prefix.json'

client = MongoClient(settings['database_url'])
database = client.SereneDB.DsActLog


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if interaction:
        return
    if error:
        return


@bot.event
async def on_guild_join(guild):
    warns = {
        'guild_id': guild.id,
        'actlogchannel': '',
        'channel_create': 'False',
        'channel_delete': 'False',
        'channel_update': 'False',
        'member_ban': 'False',
        'member_join': 'False',
        'member_kick': 'False',
        'member_leave': 'False',
        'member_unban': 'False',
        'member_update': 'False',
        'message_delete': 'False',
        'message_edit': 'False',
        'role_create': 'False',
        'role_delete': 'False',
        'role_update': 'False',
        'voice_update': 'False',
        'enabled': 'False',
    }
    if database.count_documents({'guild': guild.id}) == 0:
        database.insert_one(warns)
    with open(prefix_dir, 'r') as f:
        prefix = json.load(f)
    prefix[str(guild.id)] = '-'
    with open(prefix_dir, 'w') as w:
        json.dump(prefix, w, indent=4)


@bot.event
async def on_guild_remove(guild):
    database.delete_one({'guild_id': guild.id})


bot.run(settings['token'])
