from datetime import datetime
from settings.config import settings
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import json
import math

bot = commands.Bot(command_prefix=settings['prefix'], case_insensitive=True, intents=discord.Intents.all())


@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(len(synced))


@bot.tree.command(name='аниме',
                  description='Выводит всю информацию про аниме. ')
async def anime_search(interaction: discord.Interaction, название: str):
    name = название
    global _link, anime_url, i, text
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
    url_seacrh = f'https://shikimori.one/animes?search={name.replace(" ", "+")}'
    page = requests.get(url_seacrh, headers=header)
    soup = BeautifulSoup(page.text, "lxml")
    NothingHere = soup.find_all('div', class_='b-nothing_here')
    if NothingHere is []:
        return await interaction.response.send_message('Аниме не найдено.', ephemeral=True)
    restr = soup.find_all('p', class_='age-restricted-warning')
    if restr is []:
        for n in restr:
            i = n.text
        if str(i) == 'Доступограничен 18+':
            return await interaction.response.send_message('Не доступно в данный момент.')
    links = []
    for hr in soup.find_all('a'):
        links.append(hr.get('href'))
    try:
        anime_url = links[17]
    except IndexError:
        pass
    api_url = f'https://shikimori.org/api/animes/{anime_url.replace("https://shikimori.one/animes/", "")}'
    r = requests.get(api_url, headers=header)
    json_data = r.json()
    anime_name = json_data['name']
    russian_name_anime = json_data['russian']
    img_anime_temp = json_data['image']['original']
    img_anime = f'https://desu.shikimori.one/system/animes/preview/{str(img_anime_temp).replace("/system/animes/original/", "")}'
    description = json_data['description']
    kind = json_data['kind']
    score = json_data['score']
    status = json_data['status']
    episodes = json_data['episodes']
    episodes_aired = json_data['episodes_aired']
    released = json_data['released_on']
    rating_age = json_data['rating']
    duration_of_series = json_data['duration']
    page_a = requests.get(anime_url, headers=header)
    soup_a = BeautifulSoup(page_a.text, "lxml")
    genres = soup_a.find_all('span', class_='genre-ru')
    genres_l = str(genres).replace('<span class="genre-ru">', '')
    genres_l = genres_l.replace('</span>', '')
    genres_l = genres_l.replace('[', '')
    genres_l = genres_l.replace(']', '')
    if str(kind) == 'tv':
        kind = 'ТВ сериал.'
    if str(kind) == 'special':
        kind = 'Спешл.'
    if str(kind) == 'ova':
        kind = 'ОVA.'
    if str(kind) == 'music':
        kind = 'Клип.'
    if str(kind) == 'movie':
        kind = 'Фильм.'
    if str(kind) == 'ona':
        kind = 'ONA.'
    if str(status) == 'released':
        status = 'Вышел.'
    if str(status) == 'anons':
        status = 'Анонс.'
    if str(status) == 'ongoing':
        status = 'Онгоинг.'
    rating_age_detail = None
    if str(rating_age) == 'g':
        rating_age = 'G'
        rating_age_detail = 'Нет возрастных ограничений.'
    if str(rating_age) == 'pg_13':
        rating_age = 'PG 13'
        rating_age_detail = 'Детям до 13 лет просмотр не желателен.'
    if str(rating_age) == 'r_plus':
        rating_age = 'R+'
        rating_age_detail = 'Лицам до 17 лет просмотр запрещён.'
    if str(rating_age) == 'r':
        rating_age = 'R'
        rating_age_detail = 'Лицам до 17 лет обязательно присутствие взрослого.'
    if str(rating_age) == 'r_17':
        rating_age = 'R-17'
        rating_age_detail = 'Лицам до 17 лет обязательно присутствие взрослого.'
    if str(rating_age) == 'pg':
        rating_age = 'PG'
        rating_age_detail = 'Рекомендуется присутствие родителей.'
    if str(rating_age) == 'rx':
        rating_age = 'Rx'
        rating_age_detail = 'Хентай.'
    if len(description) > 1024:
        description = f'Описание слишком большое, просмотрите его вручную по ссылке: [Кликабельно.]({anime_url})'
    days = math.floor(duration_of_series / (24 * 60))
    total_minutes = duration_of_series
    left_minutes = total_minutes % (24 * 60)
    hours = math.floor(left_minutes / 60)
    mins = total_minutes - (days * 1440) - (hours * 60)
    duration_of_series = f'{hours} ч. {mins} м.'
    embed = discord.Embed(title='⠀', color=0x9900ff)
    embed.add_field(name='Название: ', value=f'`{anime_name}`', inline=False)
    embed.add_field(name='Русское название: ', value=f'`{russian_name_anime}`', inline=False)
    embed.add_field(name='Описание:', value=f'`{description}`', inline=False)
    embed.add_field(name='Тип: ', value=f'`{kind}`', inline=True)
    embed.add_field(name='Статус:', value=f'`{status}`', inline=True)
    embed.add_field(name='Эпизоды:', value=f'`{episodes}`', inline=True)
    embed.add_field(name='Жанры:', value=f'`{genres_l}.`', inline=False)
    embed.add_field(name='Эпизодов вышло: ', value=f'`{episodes_aired}`', inline=True)
    embed.add_field(name='Вышел в: ', value=f'`{released}`', inline=True)
    embed.add_field(name='Рейтинг:', value=f'`{rating_age}`**({rating_age_detail})**', inline=False)
    embed.add_field(name='Рейтинг аниме:', value=f'`{score}⭐`', inline=True)
    embed.add_field(name='Длительность эпизода: ', value=f'`{duration_of_series}`', inline=True)
    embed.add_field(name='Ссылка на аниме:', value=f'[Кликабельно]({anime_url})', inline=False)
    embed.set_thumbnail(url=img_anime)
    embed.set_footer(text="🤍 • Serene. Сделано с помощью shikimori.one")
    await interaction.response.send_message(embed=embed)


bot.run(settings['token'])
