from datetime import datetime
from settings.config import settings
import discord
import requests
from discord.ext import commands
from discord_together import DiscordTogether

bot = commands.Bot(command_prefix=settings['prefix'], case_insensitive=True, intents=discord.Intents.all())


@bot.event
async def on_ready():
    bot.togetherControl = await DiscordTogether(settings['token'])
    synced = await bot.tree.sync()
    print(len(synced))


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if interaction:
        return
    if error:
        return


@bot.tree.command(name='аватар', description='Показывает аватар пользователя.')
async def avatar(interaction: discord.Interaction, member: discord.Member):
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


@bot.tree.command(name='информация_о_сервере', description='Показывает информацию о сервере.')
async def serverinfo(interaction: discord.Interaction):
    embed = discord.Embed(title=f"Информация про сервер:\n{interaction.guild.name}",
                          color=discord.Colour.purple())
    embed.add_field(name='⠀', value='⠀', inline=False)
    embed.add_field(name='❖ Айди сервера:', value=f"`{interaction.guild.id}`", inline=False)
    embed.add_field(name='❖ Сервер создан:', value=f'`{interaction.guild.created_at.strftime("%d.%m.%Y, %H:%M:%S")}`',
                    inline=True)
    embed.add_field(name='❖ Владелец:', value=f"<@{interaction.guild.owner_id}>", inline=False)
    embed.add_field(name='❖ Участников:', value=f'`{interaction.guild.member_count}`', inline=True)
    embed.add_field(name='❖ Бустеров:', value=f'`{len(interaction.guild.premium_subscribers)}`', inline=False)
    embed.add_field(name='❖ Уровень бустов сервера:', value=f'`{interaction.guild.premium_tier}`')
    embed.add_field(name='❖ Бустов сервера:', value=f'`{interaction.guild.premium_subscription_count}`', inline=False)
    embed.add_field(name='❖ Ролей', value=f'`{len(interaction.guild.roles) - 1}`')
    embed.add_field(name='❖ Каналы:',
                    value=f'• **Текстовых:** `{len(interaction.guild.text_channels)}` \n  • **Голосовых:** `{len(interaction.guild.voice_channels)}`',
                    inline=False)
    embed.set_thumbnail(url=interaction.guild.icon.url)
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name='поплакать', description='Поплакать.')
async def cry(interaction: discord.Interaction):
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=cry')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff, description=f'{interaction.user.mention} плачет! >.< ')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name='обнять', description='Обнять пользователя.')
async def hug(interaction: discord.Interaction, участник: discord.Member):
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


@bot.tree.command(name='поцеловать', description='Поцеловать пользователя.')
async def kiss(interaction: discord.Interaction, участник: discord.Member):
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


@bot.tree.command(name='танцевать')
async def dance(interaction: discord.Interaction):
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=dance')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff, description=f'{interaction.user.mention} танцует! >.< ')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name='лизнуть', description='Лизнуть пользователя.')
async def lick(interaction: discord.Interaction, участник: discord.Member):
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


@bot.tree.command(name='фейспалм', description='Кринжануть.')
async def facepalm(interaction: discord.Interaction):
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=facepalm')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff,
                          description=f'{interaction.user.mention} кринажнул(-а).')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name='грустить', description='Погрустить.')
async def sad(interaction: discord.Interaction):
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=sad')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff,
                          description=f'{interaction.user.mention} грустит.')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name='улыбка', description='Улыбнуться.')
async def smug(interaction: discord.Interaction):
    r = requests.get('https://api.otakugifs.xyz/gif?reaction=smug')
    json_data = r.json()
    url = json_data['url']
    embed = discord.Embed(color=0x9900ff,
                          description=f'{interaction.user.mention} улыбнулся(-ась).')
    embed.set_image(url=url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name='извиниться', description='Извиниться перед пользователем.')
async def oh_shit_im_sorry(interaction: discord.Interaction, участник: discord.Member):
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


@bot.tree.command(name='погладить', description='Погладить по голове пользователя.')
async def pat(interaction: discord.Interaction, участник: discord.Member):
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


@bot.tree.command(name='ударить', description='Ударить пользователя.')
async def punch(interaction: discord.Interaction, участник: discord.Member):
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


@bot.tree.command(name='подмигнуть', description='Подмигнуть пользователю.')
async def wink(interaction: discord.Interaction, участник: discord.Member):
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


@bot.tree.command(name='шлёпнуть', description='Шлёпнуть пользователя.')
async def slap(interaction: discord.Interaction, участник: discord.Member):
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


bot.run(settings['token'])
