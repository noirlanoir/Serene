import datetime
from settings.config import settings
import discord
from discord.ext import commands
import json
import os

bot = commands.Bot(command_prefix=settings['prefix'], case_insensitive=True, intents=discord.Intents.all())

curr_dir = os.path.abspath(os.curdir)
project_dir = os.path.dirname(curr_dir)
prefix_dir = project_dir + '\settings\prefix.json'


@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(len(synced))


@bot.event
async def on_command_error(ctx, error):
    if ctx.message.author is None:
        pass
    if isinstance(error, discord.ext.commands.CommandNotFound):
        pass


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if interaction:
        return
    if error:
        return


timestamp = datetime.datetime.today()


@bot.tree.command(name='замутить', description='Выдает таймаут пользователю.')
async def mute(
        interaction: discord.Interaction,
        участник: discord.Member,
        время: int,
        тип: str = None,
        причина: str = None
):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message('У вас отсутствуют права администратора.', ephemeral=True)
    member = участник
    mute_time = время
    mute_type = тип
    reason = причина
    global _time, reas
    if reason is None:
        reason = 'Не указано.'
    if mute_type is None:
        return await interaction.response.send_message(embed=discord.Embed(
            title='Укажите тип  мута.',
            description='**Типы мута:**\n `д - дни, ч - часы, м - минуты, с - секунды.` \n**Пример:**\n `/mute участник: @Serene#1477 время: 30 тип: m причина: плохой пользователь.`'),
            ephemeral=True)
    if mute_type.lower() not in ['с', 'м', 'ч', 'д']:
        return await interaction.response.send_message(embed=discord.Embed(
            title='Укажите правильный тип мута.',
            description='**Типы мута:**\n `д - дни, ч - часы, м - минуты, с - секунды.` \n**Пример:**\n `/mute member: @Serene#1477 time: 30 type: m reason: плохой пользователь.`'),
            ephemeral=True)
    if mute_time <= 0:
        return await interaction.response.send_message(
            'Укажите правильное время мута. Время мута не может быть меньше либо равно 0.', ephemeral=True)
    if mute_type.lower() == 'с':
        _time = mute_time * 1
        if mute_time == 1:
            reas = 'секунда'
        elif mute_time >= 2 <= 4:
            reas = 'секунды'
        elif mute_time >= 5:
            reas = 'секунд'
    if mute_type.lower() == 'м':
        _time = mute_time * 60
        if mute_time == 1:
            reas = 'минута'
        elif mute_time >= 2 <= 4:
            reas = 'минуты'
        elif mute_time >= 5:
            reas = 'минут'
    if mute_type.lower() == 'ч':
        _time = mute_time * 3600
        if mute_time == 1:
            reas = 'час'
        elif mute_time >= 2 <= 4:
            reas = 'часа'
        elif mute_time >= 5:
            reas = 'часов'
    if mute_type.lower() == 'д':
        _time = mute_time * 86400
        if mute_time == 1:
            reas = 'день'
        elif mute_time >= 2 <= 4:
            reas = 'дня'
        elif mute_time >= 5:
            reas = 'дней'
    if not 1 <= _time <= 2_419_200:
        return await interaction.response.send_message(
            'Время таймаута должен быть не меньше 1 секунды и не больше 27 дней.', ephemeral=True
        )
    muted_until = datetime.datetime.now().astimezone() + datetime.timedelta(seconds=_time)
    try:
        await member.timeout(muted_until)
    except discord.errors.Forbidden as e:
        if str(e) == '403 Forbidden (error code: 50013): Missing Permissions':
            await interaction.response.send_message('Ошибка! У пользователя больше прав чем у бота.', ephemeral=True)
    embed_mute = discord.Embed(title=f'**Мут.**', color=0x9900ff, timestamp=datetime.datetime.utcnow())
    embed_mute.add_field(name='`Выдал:`', value=interaction.user.mention, inline=True)
    embed_mute.add_field(name='`Нарушитель:`', value=member.mention, inline=True)
    embed_mute.add_field(name='`Причина:`', value=f'{reason}', inline=False)
    embed_mute.add_field(name='`Длительность:`', value=f'{mute_time} {reas}', inline=True)
    embed_mute.add_field(name='`ID нарушителя:`', value=member.id, inline=False)
    embed_mute.add_field(name='`Выдан в:`', value=timestamp.strftime("%d.%m.%Y, %H:%M:%S"), inline=False)
    embed_mute.add_field(name='`Мут до:`', value=str(muted_until.strftime("%d.%m.%Y, %H:%M:%S")), inline=False)
    embed_mute.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon)
    embed_mute.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed_mute)


@bot.tree.command(name='анмут', description='Снимает таймаут с пользователя.')
async def unmute(
        interaction: discord.Interaction,
        участник: discord.Member
):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message('У вас отсутствуют права администратора.', ephemeral=True)
    member = участник
    if member.is_timed_out() is True:
        await member.timeout(None)
        return await interaction.response.send_message(f'Таймаут пользователю {member.mention} был успешно снят.')
    else:
        return await interaction.response.send_message(f'Ошибка! Пользователь {member.mention} не находится в муте.',
                                                       ephemeral=True)


@bot.tree.command(name='забанить', description='Банит пользователя на сервере.')
async def ban(
        interaction: discord.Interaction,
        участник: discord.Member,
        причина: str = None,
):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message('У вас отсутствуют права администратора.', ephemeral=True)
    reason = причина
    member = участник
    if reason is None:
        reason = 'Не указано.'
    try:
        await member.ban(reason=причина)
        embed_ban = discord.Embed(title=f'**Бан.**', color=0x9900ff, timestamp=datetime.datetime.utcnow())
        embed_ban.add_field(name='`Выдал:`', value=interaction.user.mention, inline=True)
        embed_ban.add_field(name='`Нарушитель:`', value=member.mention, inline=True)
        embed_ban.add_field(name='`Причина:`', value=f'{reason}', inline=False)
        embed_ban.add_field(name='`ID нарушителя:`', value=member.id, inline=False)
        embed_ban.add_field(name='`Выдан в:`', value=timestamp.strftime("%d.%m.%Y, %H:%M:%S"), inline=False)
        embed_ban.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon)
        embed_ban.set_footer(text="🤍 • Serene.")
        await interaction.response.send_message(embed=embed_ban)
    except discord.errors.Forbidden as e:
        if str(e) == '403 Forbidden (error code: 50013): Missing Permissions':
            await interaction.response.send_message('Ошибка! У пользователя больше прав чем у бота.', ephemeral=True)


@bot.tree.command(name='выгнать', description='Выгоняет пользователя с сервера.')
async def kick(
        interaction: discord.Interaction,
        участник: discord.Member,
        причина: str = None
):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message('У вас отсутствуют права администратора.', ephemeral=True)
    member = участник
    reason = причина
    if reason is None:
        reason = 'Не указано.'
    try:
        await member.kick(reason=reason)
        embed_ban = discord.Embed(title=f'**Кик.**', color=0x9900ff, timestamp=datetime.datetime.utcnow())
        embed_ban.add_field(name='`Выдал:`', value=interaction.user.mention, inline=True)
        embed_ban.add_field(name='`Нарушитель:`', value=member.mention, inline=True)
        embed_ban.add_field(name='`Причина:`', value=f'{reason}', inline=False)
        embed_ban.add_field(name='`ID нарушителя:`', value=member.id, inline=False)
        embed_ban.add_field(name='`Выдан в:`', value=timestamp.strftime("%d.%m.%Y, %H:%M:%S"), inline=False)
        embed_ban.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon)
        embed_ban.set_footer(text="🤍 • Serene.")
        await interaction.response.send_message(embed=embed_ban)
    except discord.errors.Forbidden as e:
        if str(e) == '403 Forbidden (error code: 50013): Missing Permissions':
            await interaction.response.send_message('Ошибка! У пользователя больше прав чем у бота.', ephemeral=True)


@bot.tree.command(name='сменить_префикс', description='Меняет префикс бота.')
async def setprefix(interaction: discord.Interaction, новый_префикс: str):
    new = новый_префикс
    with open(prefix_dir, 'r') as f:
        prefix = json.load(f)
    prefix[str(interaction.user.guild.id)] = new
    with open(prefix_dir, 'w') as w:
        json.dump(prefix, w, indent=4)
        await interaction.response.send_message(f'Префикс успешно сменён на {new}.')


# @bot.tree.command(name='разбанить', description='Разбанить пользователя.')
# async def unban(interaction: discord.Interaction, *, member: discord.Member):
#     if not interaction.user.guild_permissions.administrator:
#         return await interaction.response.send_message('У вас отсутствуют права администратора.', ephemeral=True)
#     if member is None:
#         embed_error = discord.Embed(title='Ошибка снятия бана.',
#                                     description=f'{interaction.user.mention}, Укажите пользователя!',
#                                     color=0x9900ff)
#         return interaction.response.send_message(embed=embed_error, ephemeral=True)
#     try:
#         banned_user = await bot.fetch_user(member.id)
#         await interaction.user.guild.unban(banned_user)
#     except discord.errors.NotFound as e:
#         if e:
#             embed_error = discord.Embed(title='Ошибка снятия бана.',
#                                         description=f'{interaction.user.mention}, Пользователь не в бане!',
#                                         color=0x9900ff)
#             return await interaction.response.send_message(embed=embed_error, ephemeral=True)
#     embed_unban = discord.Embed(title=f'**Снятие бана.**', color=0x9900ff)
#     embed_unban.add_field(name='`Снял:`', value=interaction.user.mention, inline=False)
#     embed_unban.add_field(name='`Пользователь:`', value=member.mention, inline=True)
#     embed_unban.add_field(name='`ID пользователя:`', value=member.id, inline=False)
#     embed_unban.set_footer(text=f'Дата: {times_start.strftime("%Y-%M-%d, %H:%M:%S")}')
#     embed_unban.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon)
#     return interaction.response.send_message(embed=embed_unban)

@bot.tree.command(name='префикс', description='Узнать префикс бота на этом сервере.')
async def get_server_prefix(interaction: discord.Interaction):
    with open(prefix_dir, 'r') as f:
        prefix = json.load(f)
    await interaction.response.send_message(f'Префикс бота на этом сервере: `{prefix[str(interaction.guild.id)]}`.')


@bot.tree.command()
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Понг! Я жив и ем шоколадки. `{round(bot.latency, 4)}` ms')


bot.run(settings['token'])
