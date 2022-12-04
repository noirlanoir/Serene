import datetime
from settings.config import settings
import discord
from discord.ext import commands
import json
import os
from discord import app_commands

curr_dir = os.path.abspath(os.curdir)
project_dir = os.path.dirname(curr_dir)
prefix_dir = project_dir + '\settings\prefix.json'
timestamp = datetime.datetime.today()


async def _mute(
        interaction: discord.Interaction,
        участник: discord.Member,
        время: int,
        тип: app_commands.Choice[int],
        причина: str = None
):
    if not interaction.user.guild_permissions.moderate_members:
        return await interaction.response.send_message('`У вас отсутствуют права администратора.`', ephemeral=True)
    member = участник
    mute_time = время
    reason = причина
    global _time, reas
    if member.is_timed_out() is True:
        return await interaction.response.send_message('`Пользователь уже находится в муте.`')
    if reason is None:
        reason = 'Не указано.'
    if mute_time <= 0:
        return await interaction.response.send_message(
            '`Укажите правильное время мута. Время мута не может быть меньше либо равно 0.`', ephemeral=True)
    if тип.value == 4:
        _time = mute_time * 1
        if mute_time == 1:
            reas = 'секунда'
        elif mute_time >= 2 <= 4:
            reas = 'секунды'
        elif mute_time >= 5:
            reas = 'секунд'
    if тип.value == 2:
        _time = mute_time * 60
        if mute_time == 1:
            reas = 'минута'
        elif mute_time >= 2 <= 4:
            reas = 'минуты'
        elif mute_time >= 5:
            reas = 'минут'
    if тип.value == 3:
        _time = mute_time * 3600
        if mute_time == 1:
            reas = 'час'
        elif mute_time >= 2 <= 4:
            reas = 'часа'
        elif mute_time >= 5:
            reas = 'часов'
    if тип.value == 1:
        _time = mute_time * 86400
        if mute_time == 1:
            reas = 'день'
        elif mute_time >= 2 <= 4:
            reas = 'дня'
        elif mute_time >= 5:
            reas = 'дней'
    if not 1 <= _time <= 2_419_200:
        return await interaction.response.send_message(
            '`Время таймаута должен быть не меньше 1 секунды и не больше 27 дней.`', ephemeral=True
        )
    muted_until = datetime.datetime.now().astimezone() + datetime.timedelta(seconds=_time)
    try:
        await member.timeout(muted_until)
    except discord.errors.Forbidden as e:
        if str(e) == '403 Forbidden (error code: 50013): Missing Permissions':
            await interaction.response.send_message(
                '`Ошибка! Возможно, у бота отсутствуют права, либо у пользователя их больше, чем у бота.`',
                ephemeral=True)
    embed_mute = discord.Embed(title=f'**Мут.**', color=0x9900ff, timestamp=datetime.datetime.utcnow())
    embed_mute.add_field(name='`Выдал:`', value=interaction.user.mention, inline=True)
    embed_mute.add_field(name='`Нарушитель:`', value=member.mention, inline=True)
    embed_mute.add_field(name='`Причина:`', value=f'{reason}', inline=False)
    embed_mute.add_field(name='`Длительность:`', value=f'{mute_time} {reas}', inline=True)
    embed_mute.add_field(name='`ID нарушителя:`', value=member.id, inline=False)
    embed_mute.add_field(name='`Наказание выдано в:`', value=timestamp.strftime("%d.%m.%Y, %H:%M:%S"), inline=False)
    embed_mute.add_field(name='`Мут до:`', value=str(muted_until.strftime("%d.%m.%Y, %H:%M:%S")), inline=False)
    embed_mute.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon)
    embed_mute.set_footer(text="🤍 • Serene.")
    await interaction.response.send_message(embed=embed_mute)


async def _unmute(
        interaction: discord.Interaction,
        участник: discord.Member
):
    if not interaction.user.guild_permissions.moderate_members:
        return await interaction.response.send_message('`У вас отсутствуют права на это действие.`', ephemeral=True)
    member = участник
    if member.is_timed_out() is True:
        await member.timeout(None)
        return await interaction.response.send_message(f'`Таймаут пользователю` {member.mention} `был успешно снят.`')
    else:
        return await interaction.response.send_message(f'`Ошибка! Пользователь` {member.mention} `не находится в муте.`',
                                                       ephemeral=True)


async def _ban(
        interaction: discord.Interaction,
        участник: discord.Member,
        причина: str = None,
):
    if not interaction.user.guild_permissions.ban_members:
        return await interaction.response.send_message('`У вас отсутствуют права на это действие.`', ephemeral=True)
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
        embed_ban.add_field(name='`Наказание выдано в:`', value=timestamp.strftime("%d.%m.%Y, %H:%M:%S"), inline=False)
        embed_ban.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon)
        embed_ban.set_footer(text="🤍 • Serene.")
        await interaction.response.send_message(embed=embed_ban)
    except discord.errors.Forbidden as e:
        if str(e) == '403 Forbidden (error code: 50013): Missing Permissions':
            await interaction.response.send_message(
                '`Ошибка! Возможно, у бота отсутствуют права, либо у пользователя их больше, чем у бота.`',
                ephemeral=True)


async def _kick(
        interaction: discord.Interaction,
        участник: discord.Member,
        причина: str = None
):
    if not interaction.user.guild_permissions.kick_members:
        return await interaction.response.send_message('`У вас отсутствуют права на это действие.`', ephemeral=True)
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
        embed_ban.add_field(name='`Наказание выдано в:`', value=timestamp.strftime("%d.%m.%Y, %H:%M:%S"), inline=False)
        embed_ban.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon)
        embed_ban.set_footer(text="🤍 • Serene.")
        await interaction.response.send_message(embed=embed_ban)
    except discord.errors.Forbidden as e:
        if str(e) == '403 Forbidden (error code: 50013): Missing Permissions':
            await interaction.response.send_message(
                '`Ошибка! Возможно, у бота отсутствуют права, либо у пользователя их больше, чем у бота.`',
                ephemeral=True)


async def _setprefix(interaction: discord.Interaction, новый_префикс: str):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message('`У вас отсутствуют права на это действие.`', ephemeral=True)
    new = новый_префикс
    with open(prefix_dir, 'r') as f:
        prefix = json.load(f)
    prefix[str(interaction.user.guild.id)] = new
    with open(prefix_dir, 'w') as w:
        json.dump(prefix, w, indent=4)
        await interaction.response.send_message(f'Префикс успешно сменён на {new}.')


async def _unban(interaction: discord.Interaction, айди_пользователя: str):
    member_id = айди_пользователя
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message('`У вас отсутствуют права на это действие.`', ephemeral=True)
    global banned_user
    if member_id is None:
        embed_error = discord.Embed(title='Ошибка снятия бана.',
                                    description=f'{interaction.user.mention}, Укажите id пользователя!',
                                    color=0x9900ff)
        return await interaction.response.send_message(embed=embed_error, ephemeral=True)
    try:
        banned_user = await bot.fetch_user(int(member_id))
        await interaction.guild.unban(banned_user)
        await interaction.response.send_message(f'`Пользователь` {banned_user.mention} `был разбанен.`', ephemeral=True)
    except discord.errors.NotFound:
        embed_error = discord.Embed(title='Ошибка снятия бана.',
                                    description=f'{interaction.user.mention}, Пользователь не в бане!',
                                    color=0x9900ff)
        await interaction.response.send_message(embed=embed_error, ephemeral=True)


async def _clear(interaction: discord.Interaction, количество: int):
    amount = количество
    if not interaction.user.guild_permissions.manage_messages:
        return await interaction.response.send_message('`У вас отсутствуют права на это действие.`', ephemeral=True)
    if amount <= 0:
        return await interaction.response.send_message('`Количество удаляемых сообщений должно быть больше 0.`',
                                                       ephemeral=True)
    if amount > 500:
        return await interaction.response.send_message('`Очистить за раз можно не больше 500 сообщений.`', ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f'**Удалено `{len(deleted)}` сообщений.**', ephemeral=True)


async def _get_server_prefix(interaction: discord.Interaction):
    with open(prefix_dir, 'r') as f:
        prefix = json.load(f)
    await interaction.response.send_message(f'Префикс бота на этом сервере: `{prefix[str(interaction.guild.id)]}`.',
                                            ephemeral=True)


async def _ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Понг! Я жив и ем шоколадки. `{round(bot.latency, 4)}` ms')
