from settings.config import settings
import discord
import requests
from discord.ext import commands

bot = commands.Bot(command_prefix=settings['prefix'], case_insensitive=True, intents=discord.Intents.all())


@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(len(synced))


@bot.tree.command(name='хелп', description='Показывает всю информацию о боте и команадах.')
async def help(interaction: discord.Interaction, команда: str = None):
    command = команда
    if command is None:
        embed = discord.Embed(title='Помощь.', color=0x9900ff)
        embed.add_field(name='⠀', value='⠀')
        embed.add_field(name='**1. Слэш команды.**', value='⠀')
        embed.add_field(
            name='Команды модерации:',
            value=
            '`мут`, '
            ' `анмут`, '
            '`бан`, '
            ' `кик`, '
            '`сменить префикс`, '
            '`префикс`. ',
            inline=False
        )
        embed.add_field(
            name='Развлекательные команды:',
            value=
            '`аватар`, '
            '`информация о сервере`, '
            '`поплакать`, '
            '`обнять`, '
            '`поцеловать`, '
            '`танцевать`, \n'
            '`лизнуть`, '
            '`фейспалм`, '
            '`грустить`, '
            '`улыбка`, '
            '`извиниться`, '
            '`погладить`, '
            '`ударить`, '
            '`подмигнуть`,'
            '`шлёпнуть`. ',
            inline=False
        )
        embed.add_field(name='⠀', value='⠀')
        embed.add_field(name='**2. Обычные команды.**', value='⠀')
        embed.add_field(
            name='Команды модерации:',
            value=
            '`clear`, '
            '`unban`. ', inline=False
        )
        embed.add_field(
            name='Развлекательные команды:',
            value='`info`. ', inline=False
        )
        await interaction.response.send_message(embed=embed)


bot.run(settings['token'])
