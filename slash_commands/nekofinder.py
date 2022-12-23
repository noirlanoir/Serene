import random
import requests
from bs4 import BeautifulSoup
import re
from settings.config import settings
import discord
from discord.ext import commands
import hmtai
from discord import app_commands


async def _nekofinder(interaction: discord.Interaction):
    embed = discord.Embed(color=0x9900ff)
    embed.set_image(url=hmtai.get('nekos', 'neko'))
    await interaction.response.send_message(embed=embed)
