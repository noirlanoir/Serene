from settings.config import settings
import discord
from discord.ext import commands
from entertainment_slash import _avatar, _pat, _sad, _lick, _slap, _smug, _wink, _punch, _facepalm, _reversed_str, \
    _oh_shit_im_sorry, _cry, _hug, _kiss, _dance, _serverinfo, _ratewifu
from anime_finder_slash import _anime_search
from moderation_slash import _ping, _ban, _kick, _mute, _unmute, _setprefix, _get_server_prefix
from help_slash import _help
from r34_finder_slash import _r34_finder
from hentai_imgs_search import _search_hentai

bot = commands.Bot(command_prefix=settings['prefix'], case_insensitive=True, intents=discord.Intents.all())
bot.remove_command('help')


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
                  description='Выводит всю информацию про аниме. ')
async def anime_search(interaction: discord.Interaction, название: str):
    await _anime_search(interaction, название)


@bot.tree.command(name='аватар', description='Показывает аватар пользователя.')
async def avatar(interaction: discord.Interaction, участник: discord.Member):
    member = участник
    await _avatar(interaction, member=member)


@bot.tree.command(name='пинг', description='Узнать, онлайн ли бот.')
async def ping(interaction: discord.Interaction):
    await _ping(interaction)


@bot.tree.command(name='перевернуть-текст', description='Выводит любой текст задом наперёд.')
async def reversed_str(interaction: discord.Interaction, текст: str):
    await _reversed_str(interaction, текст)


@bot.tree.command(name='шлёпнуть', description='Шлёпнуть пользователя.')
async def slap(interaction: discord.Interaction, участник: discord.Member):
    await _slap(interaction, участник)


@bot.tree.command(name='подмигнуть', description='Подмигнуть пользователю.')
async def wink(interaction: discord.Interaction, участник: discord.Member):
    await _wink(interaction, участник)


@bot.tree.command(name='ударить', description='Ударить пользователя.')
async def punch(interaction: discord.Interaction, участник: discord.Member):
    await _punch(interaction, участник)


@bot.tree.command(name='погладить', description='Погладить по голове пользователя.')
async def pat(interaction: discord.Interaction, участник: discord.Member):
    await _pat(interaction, участник)


@bot.tree.command(name='извиниться', description='Извиниться перед пользователем.')
async def oh_shit_im_sorry(interaction: discord.Interaction, участник: discord.Member):
    await _oh_shit_im_sorry(interaction, участник)


@bot.tree.command(name='улыбка', description='Улыбнуться.')
async def smug(interaction: discord.Interaction):
    await _smug(interaction)


@bot.tree.command(name='грустить', description='Погрустить.')
async def sad(interaction: discord.Interaction):
    await _sad(interaction)


@bot.tree.command(name='фейспалм', description='Кринжануть.')
async def facepalm(interaction: discord.Interaction):
    await _facepalm(interaction)


@bot.tree.command(name='лизнуть', description='Лизнуть пользователя.')
async def lick(interaction: discord.Interaction, участник: discord.Member):
    await _lick(interaction, участник)


@bot.tree.command(name='танцевать')
async def dance(interaction: discord.Interaction):
    await _dance(interaction)


@bot.tree.command(name='поцеловать', description='Поцеловать пользователя.')
async def kiss(interaction: discord.Interaction, участник: discord.Member):
    await _kiss(interaction, участник)


@bot.tree.command(name='обнять', description='Обнять пользователя.')
async def hug(interaction: discord.Interaction, участник: discord.Member):
    await _hug(interaction, участник)


@bot.tree.command(name='поплакать', description='Поплакать на общее обозрение.')
async def cry(interaction: discord.Interaction):
    await _cry(interaction)


@bot.tree.command(name='информация-о-сервере', description='Показывает информацию о сервере.')
async def serverinfo(interaction: discord.Interaction):
    await _serverinfo(interaction)


@bot.tree.command(name='префикс', description='Узнать префикс бота на этом сервере.')
async def get_server_prefix(interaction: discord.Interaction):
    await _get_server_prefix(interaction)


@bot.tree.command(name='сменить-префикс', description='Меняет префикс бота.')
async def setprefix(interaction: discord.Interaction, новый_префикс: str):
    await _setprefix(interaction, новый_префикс)


@bot.tree.command(name='выгнать', description='Выгоняет пользователя с сервера.')
async def kick(
        interaction: discord.Interaction,
        участник: discord.Member,
        причина: str = None
):
    await _kick(interaction, участник, причина)


@bot.tree.command(name='забанить', description='Банит пользователя на сервере.')
async def ban(
        interaction: discord.Interaction,
        участник: discord.Member,
        причина: str = None,
):
    await _ban(interaction, участник, причина)


@bot.tree.command(name='анмут', description='Снимает таймаут с пользователя.')
async def unmute(
        interaction: discord.Interaction,
        участник: discord.Member
):
    await _unmute(interaction, участник)


@bot.tree.command(name='замутить', description='Выдает таймаут пользователю.')
async def mute(
        interaction: discord.Interaction,
        участник: discord.Member,
        время: int,
        тип: str = None,
        причина: str = None
):
    await _mute(interaction, участник, время, тип, причина)


@bot.tree.command(name='хелп', description='Информация о командах бота.')
async def help(interaction: discord.Interaction, команда: str = None):
    await _help(interaction, команда)


@bot.tree.command(name='оценить-вайфу', description='Оценивает пользователя по 10-бальной шкале.')
async def ratewifu(interaction: discord.Interaction, участник: discord.Member):
    await _ratewifu(interaction, участник)


# @bot.tree.command(name='r34', description='Поиск rule34 картинок по запросу. Примечание: запрос желателен на английском языке.')
# async def r34(interaction: discord.Interaction, запрос: str):
#    await _r34(interaction, запрос)


@bot.tree.command(name='хентай',
                  description='Поиск хентай картинок. Примечание: запрос должен быть на английском языке.')
async def search_hentai(interaction: discord.Interaction, поиск: str):
    await _search_hentai(interaction, поиск)


bot.run(settings['token'])
