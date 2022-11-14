import random
import requests
from bs4 import BeautifulSoup
import re
from settings.config import settings
import discord
from discord.ext import commands

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
             (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}


async def _search_hentai(interaction: discord.Interaction, поиск: str):
    search = поиск
    if not interaction.channel.is_nsfw() is True:
        return await interaction.response.send_message(
            '`В данном канале не включен nsfw режим. Включите его, для того чтобы использовать эту команду.`',
            ephemeral=True)
    url = f'https://hentai-img.com/search/keyword/{search}/page/1/'
    r = requests.get(url, headers=header)
    b = BeautifulSoup(r.text, 'lxml')
    images = b.find_all('img')

    n = 0
    i = 0

    imgs = []
    while i < len(images):
        if 'https://static1' in str(images[i]):
            imgs.append(images[i])
        i += 1

    new_img_list = []
    while n < len(imgs):
        new_img_list.append((str(imgs[n]).replace('<img loading="lazy" src="', '')).replace('"/>', ""))
        n += 1
    try:
        random_url = random.choice(new_img_list)
    except IndexError:
        return await interaction.response.send_message('`По вашему запросу ничего не найдено.`', ephemeral=True)
    embed = discord.Embed(title='Вот, что нашлось по запросу:',
                          description=f'[Если картинка не прогрузилась, нажмите сюда]({random_url})', color=0x9900ff)
    await interaction.channel.send(random_url)
    await interaction.response.send_message(embed=embed)
