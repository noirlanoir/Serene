from settings.config import settings
import discord
from pymongo import MongoClient
from discord import app_commands
from discord.ext import commands
from entertainment_slash import _avatar, _pat, _sad, _lick, _slap, _smug, _wink, _punch, _facepalm, _reversed_str, \
    _oh_shit_im_sorry, _cry, _hug, _kiss, _dance, _serverinfo, _ratewifu
from anime_finder_slash import _anime_search
from moderation_slash import _ping, _ban, _kick, _mute, _unmute, _setprefix, _get_server_prefix, _clear, _unban
from help_slash import _help
from hentai_imgs_search import _search_hentai
from nekofinder import _nekoFinder

bot = commands.Bot(command_prefix=settings['prefix'], case_insensitive=True, intents=discord.Intents.all())
bot.remove_command('help')

client = MongoClient(settings['database_url'])
database = client.SereneDB.DsActLog


@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(len(synced))


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if interaction:
        return
    if error:
        return


@bot.event
async def on_command_error(ctx, error):
    if ctx.message.author is None:
        pass
    if isinstance(error, discord.ext.commands.CommandNotFound):
        pass


@bot.tree.command(name='аниме',
                  description='Выводит всю информацию про аниме ')
async def anime_search(interaction: discord.Interaction, название: str):
    await _anime_search(interaction, название)


@bot.tree.command(name='аватар', description='Показывает аватар пользователя')
async def avatar(interaction: discord.Interaction, участник: discord.Member):
    member = участник
    await _avatar(interaction, member=member)


@bot.tree.command(name='пинг', description='Узнать, онлайн ли бот')
async def ping(interaction: discord.Interaction):
    await _ping(interaction)


@bot.tree.command(name='clear', description='Очищает сообщения в канале.')
async def clear(interaction: discord.Interaction, количество: int):
    await _clear(interaction, количество)


@bot.tree.command(name='разбанить', description='Разбанить пользователя.')
async def unban(interaction: discord.Interaction, айди: str):
    await _unban(interaction, айди_пользователя=айди)


@bot.tree.command(name='перевернуть-текст', description='Выводит любой текст отзеркаленным')
async def reversed_str(interaction: discord.Interaction, текст: str):
    await _reversed_str(interaction, текст)


@bot.tree.command(name='шлёпнуть', description='Шлёпнуть пользователя')
async def slap(interaction: discord.Interaction, участник: discord.Member):
    await _slap(interaction, участник)


@bot.tree.command(name='подмигнуть', description='Подмигнуть пользователю')
async def wink(interaction: discord.Interaction, участник: discord.Member):
    await _wink(interaction, участник)


@bot.tree.command(name='ударить', description='Ударить пользователя')
async def punch(interaction: discord.Interaction, участник: discord.Member):
    await _punch(interaction, участник)


@bot.tree.command(name='погладить', description='Погладить по голове пользователя')
async def pat(interaction: discord.Interaction, участник: discord.Member):
    await _pat(interaction, участник)


@bot.tree.command(name='извиниться', description='Извиниться перед пользователем')
async def oh_shit_im_sorry(interaction: discord.Interaction, участник: discord.Member):
    await _oh_shit_im_sorry(interaction, участник)


@bot.tree.command(name='улыбка', description='Улыбнуться')
async def smug(interaction: discord.Interaction):
    await _smug(interaction)


@bot.tree.command(name='грустить', description='Погрустить')
async def sad(interaction: discord.Interaction):
    await _sad(interaction)


@bot.tree.command(name='фейспалм', description='Кринжануть')
async def facepalm(interaction: discord.Interaction):
    await _facepalm(interaction)


@bot.tree.command(name='лизнуть', description='Лизнуть кого нибудь')
async def lick(interaction: discord.Interaction, участник: discord.Member):
    await _lick(interaction, участник)


@bot.tree.command(name='танцевать')
async def dance(interaction: discord.Interaction):
    await _dance(interaction)


@bot.tree.command(name='поцеловать', description='Поцеловать пользователя')
async def kiss(interaction: discord.Interaction, участник: discord.Member):
    await _kiss(interaction, участник)


@bot.tree.command(name='обнять', description='Обнять пользователя')
async def hug(interaction: discord.Interaction, участник: discord.Member):
    await _hug(interaction, участник)


@bot.tree.command(name='поплакать', description='Поплакать на общее обозрение')
async def cry(interaction: discord.Interaction):
    await _cry(interaction)


@bot.tree.command(name='информация-о-сервере', description='Показывает информацию о сервере')
async def serverinfo(interaction: discord.Interaction):
    await _serverinfo(interaction)


@bot.tree.command(name='префикс', description='Узнать префикс бота на этом сервере')
async def get_server_prefix(interaction: discord.Interaction):
    await _get_server_prefix(interaction)


@bot.tree.command(name='сменить-префикс', description='Меняет префикс бота')
async def setprefix(interaction: discord.Interaction, новый_префикс: str):
    await _setprefix(interaction, новый_префикс)


@bot.tree.command(name='кик', description='Выгоняет пользователя с сервера')
async def kick(
        interaction: discord.Interaction,
        участник: discord.Member,
        причина: str = None
):
    await _kick(interaction, участник, причина)


@bot.tree.command(name='бан', description='Банит пользователя на сервере')
async def ban(
        interaction: discord.Interaction,
        участник: discord.Member,
        причина: str = None,
):
    await _ban(interaction, участник, причина)


@bot.tree.command(name='анмут', description='Снимает таймаут с пользователя')
async def unmute(
        interaction: discord.Interaction,
        участник: discord.Member
):
    await _unmute(interaction, участник)


@bot.tree.command(name='мут', description='Выдает таймаут пользователю')
@app_commands.choices(тип=[
    discord.app_commands.Choice(name='дни', value=1),
    discord.app_commands.Choice(name='минуты', value=2),
    discord.app_commands.Choice(name='часы', value=3),
    discord.app_commands.Choice(name='секунды', value=4),
])
async def mute(
        interaction: discord.Interaction,
        участник: discord.Member,
        время: int,
        тип: app_commands.Choice[int],
        причина: str = None
):
    await _mute(interaction, участник, время, тип, причина)


@bot.tree.command(name='хелп', description='Информация о командах бота')
async def help(interaction: discord.Interaction, команда: str = None):
    await _help(interaction, команда)


@bot.tree.command(name='оценить-вайфу', description='Оценивает пользователя по 10-бальной шкале')
async def ratewifu(interaction: discord.Interaction, участник: discord.Member):
    await _ratewifu(interaction, участник)


@bot.tree.command(name='nsfw-картинки',
                  description='Поиск непристойных изображений!')
@app_commands.choices(поиск=[
    discord.app_commands.Choice(name='anal(анал)', value='anal'),
    discord.app_commands.Choice(name='ass(попка)', value='ass'),
    discord.app_commands.Choice(name='bdsm(бдсм)', value='bdsm'),
    discord.app_commands.Choice(name='cum(малафья)', value='cum'),
    discord.app_commands.Choice(name='classic(классическое)', value='classic'),
    discord.app_commands.Choice(name='creampie(кремпайчик)', value='creampie'),
    discord.app_commands.Choice(name='femdom(доминация девушек)', value='femdom'),
    discord.app_commands.Choice(name='hentai(рандом хентайчик)', value='hentai'),
    discord.app_commands.Choice(name='incest(инцест)', value='incest'),
    discord.app_commands.Choice(name='masturbation(мастурбация)', value='femdom'),
    discord.app_commands.Choice(name='public(в публичном месте)', value='public'),
    discord.app_commands.Choice(name='ero(эро)', value='ero'),
    discord.app_commands.Choice(name='orgy(оргия)', value='orgy'),
    discord.app_commands.Choice(name='elves(эльфочки)', value='elves'),
    discord.app_commands.Choice(name='yuri(лесбиянки)', value='yuri'),
    discord.app_commands.Choice(name='pantsu(трусики)', value='pantsu'),
    discord.app_commands.Choice(name='blowjob(минетик)', value='blowjob'),
    discord.app_commands.Choice(name='boobjob(работа грудью)', value='boobjob'),
    discord.app_commands.Choice(name='footjob(работа ножками)', value='footjob'),
    discord.app_commands.Choice(name='handjob(работа ручками)', value='handjob'),
    discord.app_commands.Choice(name='boobs(сисечки)', value='boobs'),
    discord.app_commands.Choice(name='pussy(писечка)', value='pussy'),
    discord.app_commands.Choice(name='uniform(униформа)', value='uniform'),
    discord.app_commands.Choice(name='tentacles(тентакли)', value='tentacles'),
    discord.app_commands.Choice(name='nsfwNeko(кошкодевочки)', value='nsfwNeko'),
])
async def search_hentai(interaction: discord.Interaction, поиск: app_commands.Choice[str]):
    await _search_hentai(interaction, поиск)


@bot.tree.command(name='r34',
                  description='Поиск rule34 картинок по запросу. Примечание: запрос желателен на английском языке')
async def r34(interaction: discord.Interaction, запрос: str):
    await _r34(interaction, запрос)


@bot.tree.command(name='логи-информация', description='Просмотреть статус всех опций логирования на этом сервере')
async def _logs_information(interaction: discord.Interaction):
    isEnabled = database.find_one({'guild_id': interaction.guild.id})['enabled']
    logChannel = database.find_one({'guild_id': interaction.guild.id})['actlogchannel']
    isEnabledChannelCreate = database.find_one({'guild_id': interaction.guild.id})['channel_create']
    isEnabledChannelDelete = database.find_one({'guild_id': interaction.guild.id})['channel_delete']
    isEnabledChannelUpdate = database.find_one({'guild_id': interaction.guild.id})['channel_update']
    isEnabledMemberJoin = database.find_one({'guild_id': interaction.guild.id})['member_join']
    isEnabledMemberLeave = database.find_one({'guild_id': interaction.guild.id})['member_leave']
    isEnabledMemberBan = database.find_one({'guild_id': interaction.guild.id})['member_ban']
    isEnabledMemberKick = database.find_one({'guild_id': interaction.guild.id})['member_kick']
    isEnabledMemberUnban = database.find_one({'guild_id': interaction.guild.id})['member_unban']
    isEnabledMemberUpdate = database.find_one({'guild_id': interaction.guild.id})['member_update']
    isEnabledVoiceUpdate = database.find_one({'guild_id': interaction.guild.id})['voice_update']
    isEnabledMessageDelete = database.find_one({'guild_id': interaction.guild.id})['message_delete']
    isEnabledMessageEdit = database.find_one({'guild_id': interaction.guild.id})['message_edit']
    isEnabledRoleCreate = database.find_one({'guild_id': interaction.guild.id})['role_create']
    isEnabledRoleDelete = database.find_one({'guild_id': interaction.guild.id})['role_delete']
    isEnabledRoleUpdate = database.find_one({'guild_id': interaction.guild.id})['role_update']
    if logChannel == '':
        val = '`Отсутствует`'
    else:
        val = f'Айди: `{logChannel}`'
    embed = discord.Embed(title='Информация об опциях:',
                          description='`В данной информации представлены статусы опций логирования на этом сервере.`',
                          color=0x9900ff)
    embed.add_field(name='enabled', value=f'{"`Включено`" if isEnabled == "True" else "`Выключено`"}', inline=False)
    embed.add_field(name='actionlogchannel', value=f'{val}',
                    inline=False)
    embed.add_field(name='channel_create',
                    value=f'{"`Включено`" if isEnabledChannelCreate == "True" else "`Выключено`"}', inline=False)
    embed.add_field(name='channel_delete',
                    value=f'{"`Включено`" if isEnabledChannelDelete == "True" else "`Выключено`"}', inline=False)
    embed.add_field(name='channel_update',
                    value=f'{"`Включено`" if isEnabledChannelUpdate == "True" else "`Выключено`"}',
                    inline=False)
    embed.add_field(name='member_join', value=f'{"`Включено`" if isEnabledMemberJoin == "True" else "`Выключено`"}',
                    inline=False)
    embed.add_field(name='member_leave', value=f'{"`Включено`" if isEnabledMemberLeave == "True" else "`Выключено`"}',
                    inline=False)
    embed.add_field(name='member_kick', value=f'{"`Включено`" if isEnabledMemberKick == "True" else "`Выключено`"}',
                    inline=False)
    embed.add_field(name='member_ban', value=f'{"`Включено`" if isEnabledMemberBan == "True" else "`Выключено`"}',
                    inline=False)
    embed.add_field(name='member_unban', value=f'{"`Включено`" if isEnabledMemberUnban == "True" else "`Выключено`"}',
                    inline=False)
    embed.add_field(name='member_update',
                    value=f'{"`Включено`" if isEnabledMemberUpdate == "True" else "`Выключено`"}',
                    inline=False)
    embed.add_field(name='voice_update',
                    value=f'{"`Включено`" if isEnabledVoiceUpdate == "True" else "`Выключено`"}', inline=False)
    embed.add_field(name='message_delete',
                    value=f'{"`Включено`" if isEnabledMessageDelete == "True" else "`Выключено`"}', inline=False)
    embed.add_field(name='message_edit', value=f'{"`Включено`" if isEnabledMessageEdit == "True" else "`Выключено`"}',
                    inline=False)
    embed.add_field(name='role_create', value=f'{"`Включено`" if isEnabledRoleCreate == "True" else "`Выключено`"}',
                    inline=False)
    embed.add_field(name='role_delete', value=f'{"`Включено`" if isEnabledRoleDelete == "True" else "`Выключено`"}',
                    inline=False)
    embed.add_field(name='role_update', value=f'{"`Включено`" if isEnabledRoleUpdate == "True" else "`Выключено`"}',
                    inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name='логи-хелп-информация', description='Помощь по опциям логов')
async def logs_help_information(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message('`У вас отсутствуют права на это действие.`', ephemeral=True)
    embed = discord.Embed(title='Информация о логах:',
                          description='**В данной информации представлены опции для логирования, для установки их:** `/логи-управление [тип] [True/False(Включить/Выключить)]`',
                          color=0x9900ff)
    embed.add_field(name='enabled', value='`[True/False] Включает функцию логирования действий.`', inline=False)
    embed.add_field(name='actionlogchannel',
                    value='`Устанавливает канал, где логируются действия.(/лог-канал-настройка)`', inline=False)
    embed.add_field(name='channel_create', value='`Логирование создания текстового/голосового каналов.`', inline=False)
    embed.add_field(name='channel_delete', value='`Логирование удаления текстового/голосового каналов.`', inline=False)
    embed.add_field(name='channel_update', value='`Логирование обновления текстового/голосового каналов.`',
                    inline=False)
    embed.add_field(name='member_join', value='`Логирование захода пользователя на сервер.`', inline=False)
    embed.add_field(name='member_ban', value='`Логирование бана пользователя.`', inline=False)
    embed.add_field(name='member_leave', value='`Логирование выхода пользователя с сервера.`', inline=False)
    embed.add_field(name='member_kick', value='`Логирование кика пользователя с сервера.`', inline=False)
    embed.add_field(name='member_unban', value='`Логирование разбана пользователя.`', inline=False)
    embed.add_field(name='member_update',
                    value='`Логирование обновление пользователя(изменение ника/обновление ролей).`',
                    inline=False)
    embed.add_field(name='voice_update',
                    value='`Логирование захода/перемещения/выхода пользователя в голосовых каналах.`', inline=False)
    embed.add_field(name='message_delete', value='`Логирование удаления сообщения.`', inline=False)
    embed.add_field(name='message_edit', value='`Логирование редактирования сообщения.`', inline=False)
    embed.add_field(name='role_create', value='`Логирование создания роли.`', inline=False)
    embed.add_field(name='role_delete', value='`Логирование удаление роли.`', inline=False)
    embed.add_field(name='role_update', value='`Логирование обновления(изменение цвета/имени) роли.`', inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name='логи-управление', description='Управление опциями логов')
@app_commands.choices(опция=[
    discord.app_commands.Choice(name='enable', value="enabled"),
    discord.app_commands.Choice(name='channel_create', value="channel_create"),
    discord.app_commands.Choice(name='channel_delete', value='channel_delete'),
    discord.app_commands.Choice(name='channel_update', value="channel_update"),
    discord.app_commands.Choice(name='member_join', value="member_join"),
    discord.app_commands.Choice(name='member_leave', value="member_leave"),
    discord.app_commands.Choice(name='member_kick', value="member_kick"),
    discord.app_commands.Choice(name='member_unban', value="member_unban"),
    discord.app_commands.Choice(name='member_update', value="member_update"),
    discord.app_commands.Choice(name='voice_update', value="voice_update"),
    discord.app_commands.Choice(name='message_delete', value="message_delete"),
    discord.app_commands.Choice(name='message_edit', value="message_edit"),
    discord.app_commands.Choice(name='role_create', value="role_create"),
    discord.app_commands.Choice(name='role_delete', value="role_delete"),
    discord.app_commands.Choice(name='role_update', value="role_update"),
])
@app_commands.choices(действие=[
    discord.app_commands.Choice(name='Включить', value=1),
    discord.app_commands.Choice(name='Выключить', value=2),
])
async def actionlog_settings(interaction: discord.Interaction, опция: app_commands.Choice[str],
                             действие: app_commands.Choice[int]):
    global enabled, _type
    type = опция
    t = действие
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message('`У вас отсутствуют права на это действие.`', ephemeral=True)
    try:
        database.find_one({'guild_id': interaction.guild.id})[f'{type.value}']
    except KeyError:
        return await interaction.response.send_message('`Тип логов не найден, просмотрите /логи-информация.`',
                                                       ephemeral=True)
    if t.value == 1:
        isEnabled = database.find_one({'guild_id': interaction.guild.id})[f'{type.value}']
        if isEnabled == 'True':
            return await interaction.response.send_message('`Выбранный тип логов уже включен.`', ephemeral=True)
        else:
            enabled = 'Включено'
            _type = 'True'
    if t.value == 2:
        isOff = database.find_one({'guild_id': interaction.guild.id})[f'{type.value}']
        if isOff == 'False':
            return await interaction.response.send_message('`Выбранный тип логов уже выключен.`', ephemeral=True)
        else:
            enabled = 'Выключено'
            _type = 'False'
    database.update_one({'guild_id': interaction.guild.id},
                        {'$set': {f'{type.value}': _type}}
                        )
    await interaction.response.send_message(f'**Опция** `{type.value}` **изменена на** `"{enabled}"`.',
                                            ephemeral=True)


@bot.tree.command(name='лог-канал-настройка', description='Настройка канала логов')
async def actionlog(interaction: discord.Interaction, канал: discord.TextChannel):
    log_channel_id = канал.id
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message('`У вас отсутствуют права на это действие.`', ephemeral=True)
    database.update_one({'guild_id': interaction.guild.id},
                        {'$set': {'actlogchannel': log_channel_id}}
                        )
    await interaction.response.send_message(f'Айди канала логов изменен на `{log_channel_id}`.', ephemeral=True)


@bot.tree.command(name='логи-управление-все', description='Включить/выключить все опции логов')
@app_commands.choices(действие=[
    discord.app_commands.Choice(name='Включить', value=1),
    discord.app_commands.Choice(name='Выключить', value=2),
])
async def log_settings_all(interaction: discord.Interaction, действие: app_commands.Choice[int], ):
    t = действие
    all_set = [
        'channel_create',
        'channel_delete',
        'channel_update',
        'role_create',
        'role_delete',
        'role_update',
        'voice_update',
        'enabled',
        'member_ban',
        'member_join',
        'member_kick',
        'member_leave',
        'member_unban',
        'member_update',
        'message_delete',
        'message_edit',
    ]
    if t.value == 1:
        i = 0
        while i < len(all_set):
            database.update_one({'guild_id': interaction.guild.id},
                                {'$set': {f'{all_set[i]}': 'True'}}
                                )

            i += 1
        return await interaction.response.send_message('`Все настройки были включены.`', ephemeral=True)
    if t.value == 2:
        i = 0
        while i < len(all_set):
            database.update_one({'guild_id': interaction.guild.id},
                                {'$set': {f'{all_set[i]}': 'False'}}
                                )
            i += 1
        await interaction.response.send_message('`Все настройки были выключены.`', ephemeral=True)


@bot.tree.command(name='неко', description='Картинка кошкодевочки!')
async def nekoFinder(interaction: discord.Interaction):
    await _nekoFinder(interaction)


bot.run(settings['token'])
