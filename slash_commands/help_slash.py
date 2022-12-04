from settings.config import settings
import discord
import requests
from discord.ext import commands
import os
import json


async def _help(interaction: discord.Interaction, команда: str = None):
    global c_d
    command = команда
    if command is None:
        embed = discord.Embed(title='⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Помощь.', color=0x9900ff)
        embed.add_field(name='⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀**1. Слэш команды.**', value='⠀')
        embed.add_field(
            name='Команды модерации:',
            value='`мут`, '
                  '`анмут`, '
                  '`бан`, '
                  '`кик`, '
                  '`сменить-префикс`, '
                  '`префикс`, \n'
                  '`логи-хелп-информация`,'
                  '`логи-управление`,\n'
                  '`лог-канал-настройка`,'
                  '`логи-управление-все`,\n'
                  '`clear`,'
                  '`unban`.',
            inline=False
        )
        embed.add_field(
            name='Развлекательные команды:',
            value='`аватар`, '
                  '`информация-о-сервере`, '
                  '`поплакать`, '
                  '`обнять`, \n'
                  '`поцеловать`, '
                  '`танцевать`, \n'
                  '`лизнуть`, '
                  '`фейспалм`, '
                  '`грустить`, '
                  '`улыбка`, '
                  '`извиниться`, \n'
                  '`погладить`, '
                  '`ударить`, '
                  '`подмигнуть`,'
                  '`шлёпнуть`, '
                  '`перевернуть-текст`,'
                  '`оценить-вайфу`,'
                  '`nsfw-картинки`,'
                  '`неко.`',
            inline=False
        )
        embed.add_field(name='⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀**2. Обычные команды.**', value='⠀')
        embed.add_field(
            name='Развлекательные команды:',
            value='`info`. ', inline=False
        )
        embed.add_field(name='⠀', value='⠀', inline=False)
        embed.add_field(name='Доп. возможности:',
                        value='`Для того чтобы узнать описание команды,\nвпишите ее после /хелп.\nВсе команды с пометкой "[/]" являются слэш командами.\nВсе команды с пометкой "[Prefix]" являются командами,\nкоторые работают по префиксу бота.`')
        embed.set_thumbnail(url=interaction.guild.icon.url)
        embed.set_footer(text="🤍 • Serene.")
        await interaction.response.send_message(embed=embed)
    if command:
        curr_dir = (os.path.abspath(os.curdir))
        project_dir = os.path.dirname(curr_dir)
        commands_dir = project_dir + '\help_module\commands_descr.json'
        with open(commands_dir, 'r', encoding='utf8') as f:
            command_js = json.load(f)
        try:
            c_d = command.lower()
            return await interaction.response.send_message(f'Команда: `{c_d}`\nОписание: `{command_js[c_d]}`',
                                                           ephemeral=True)
        except KeyError:
            await interaction.response.send_message(
                f'Команда `{c_d}` не найдена. Проверьте правильность написания команды либо просмотрите весь список через `/help`.',
                ephemeral=True)
