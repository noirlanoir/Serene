import random
import requests
from bs4 import BeautifulSoup
import re
from settings.config import settings
import discord
from discord.ext import commands
import hmtai
from discord import app_commands


async def _search_hentai(interaction: discord.Interaction, поиск: app_commands.Choice[str]):
    if not interaction.channel.is_nsfw() is True:
        return await interaction.response.send_message(
            '`В этом канале нельзя искать такое! Включите NSFW режим, чтобы использовать эту команду!`',
            ephemeral=True)
    embed = discord.Embed(title='⠀', color=0x9900ff)
    embed.set_image(url=hmtai.get('hmtai', f'{поиск.value}'))
    await interaction.response.send_message(embed=embed)
