import random
from datetime import datetime
from settings.config import settings
import discord
import requests
from discord.ext import commands


async def _avatar(interaction: discord.Interaction, member: discord.Member):
    if member is None:
        embed = discord.Embed(
            title=f'Аватар {interaction.user.display_name}',
            colour=0x9900ff
        )
        embed.set_image(url=interaction.user.avatar)
        embed.timestamp = datetime.utcnow()
        return await interaction.response.send_message(embed=embed)
    if member:
        embed = discord.Embed(
            title=f'Аватар {member.display_name}',
            colour=0x9900ff
        )
        embed.set_image(url=member.avatar)
        embed.timestamp = datetime.utcnow()
        return await interaction.response.send_message(embed=embed)


async def _serverinfo(interaction: discord.Interaction):
    embed = discord.Embed(title=f"Информация про сервер:\n{interaction.guild.name}",
                          color=discord.Colour.purple())
    embed.add_field(name='❖ Айди сервера:', value=f"`{interaction.guild.id}`", inline=False)
    embed.add_field(name='❖ Сервер создан:', value=f'`{interaction.guild.created_at.strftime("%d.%m.%Y, %H:%M:%S")}`',
                    inline=True)
    embed.add_field(name='❖ Владелец:', value=f"<@{interaction.guild.owner_id}>", inline=False)
    embed.add_field(name='❖ Участников:', value=f'`{interaction.guild.member_count}`', inline=True)
    embed.add_field(name='❖ Бустеров:', value=f'`{len(interaction.guild.premium_subscribers)}`', inline=False)
    embed.add_field(name='❖ Уровень бустов сервера:', value=f'`{interaction.guild.premium_tier}`')
    embed.add_field(name='❖ Бустов сервера:', value=f'`{interaction.guild.premium_subscription_count}`', inline=False)
    embed.add_field(name='❖ Эмодзи:', value=f'`{len(interaction.guild.emojis)}`', inline=False)
    embed.add_field(name='❖ Стикеров:', value=f'`{len(interaction.guild.stickers)}`', inline=False)
    embed.add_field(name='❖ Ролей', value=f'`{len(interaction.guild.roles) - 1}`')
    embed.add_field(name='❖ Каналы:',
                    value=f' • **Текстовых:** `{len(interaction.guild.text_channels)}` \n   • **Голосовых:** `{len(interaction.guild.voice_channels)}`',
                    inline=False)
    embed.set_thumbnail(url=interaction.guild.icon.url)
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


async def _cry(interaction: discord.Interaction):
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=cry')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff, description=f'{interaction.user.mention} плачет! >.< ')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


async def _hug(interaction: discord.Interaction, участник: discord.Member):
    member = участник
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=hug')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff,
                          description=f'{interaction.user.mention} обнял(-а) {member.mention}!')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    return await interaction.response.send_message(embed=embed)


async def _kiss(interaction: discord.Interaction, участник: discord.Member):
    member = участник
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=kiss')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff,
                          description=f'{interaction.user.mention} поцеловал(-а) {member.mention}!')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


async def _dance(interaction: discord.Interaction):
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=dance')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff, description=f'{interaction.user.mention} танцует! >.< ')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


async def _lick(interaction: discord.Interaction, участник: discord.Member):
    member = участник
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=lick')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff,
                          description=f'{interaction.user.mention} лизнул(-а) {member.mention}!')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


async def _facepalm(interaction: discord.Interaction):
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=facepalm')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff,
                          description=f'{interaction.user.mention} кринажнул(-а).')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


async def _sad(interaction: discord.Interaction):
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=sad')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff,
                          description=f'{interaction.user.mention} грустит.')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


async def _smug(interaction: discord.Interaction):
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=smug')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff,
                          description=f'{interaction.user.mention} улыбнулся(-ась).')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


async def _oh_shit_im_sorry(interaction: discord.Interaction, участник: discord.Member):
    member = участник
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=sorry')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff,
                          description=f'{interaction.user.mention} извинился(-ась) перед {member.mention}.')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


async def _pat(interaction: discord.Interaction, участник: discord.Member):
    member = участник
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=pat')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff,
                          description=f'{interaction.user.mention} погладил(-а) по голове {member.mention}!')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


async def _punch(interaction: discord.Interaction, участник: discord.Member):
    member = участник
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=punch')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff,
                          description=f'{interaction.user.mention} ударил(-а) {member.mention}!')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


async def _wink(interaction: discord.Interaction, участник: discord.Member):
    member = участник
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=wink')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff,
                          description=f'{interaction.user.mention} подмигнул(-а) {member.mention}!')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


async def _slap(interaction: discord.Interaction, участник: discord.Member):
    member = участник
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=slap')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff,
                          description=f'{interaction.user.mention} шлёпнул(-а) {member.mention}!')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


async def _reversed_str(interaction: discord.Interaction, текст: str):
    await interaction.response.send_message(f'Перевернутый текст: **{текст[::-1]}**')


async def _ratewifu(interaction: discord.Interaction, участник: discord.Member):
    member = участник
    RandNum = random.randint(1, 10)
    await interaction.response.send_message(f'**Я бы дала {member.mention} **`{RandNum}/10.`')
