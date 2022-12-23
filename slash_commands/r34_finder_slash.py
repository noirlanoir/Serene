import asyncio
from settings.config import settings
import discord
from discord.ext import commands
from rule34Py import rule34Py

bot = commands.Bot(command_prefix=settings['prefix'], case_insensitive=True, intents=discord.Intents.all())
bot.remove_command('help')


async def _r34_finder(interaction: discord.Interaction, запрос: str):
    global result
    search = запрос
    if not interaction.channel.is_nsfw() is True:
        return await interaction.response.send_message(
            '`В данном канале не включен nsfw режим, включите его, для того чтобы использовать эту команду.`',
            ephemeral=True)
    r34Py = rule34Py()
    try:
        result = r34Py.random_post([f"{search}"])
    except IndexError:
        return await interaction.response.send_message('`По вашему запросу ничего не найдено.`', ephemeral=True)
    if str(result) == '[]':
        return await interaction.response.send_message('`По вашему запросу ничего не найдено.`', ephemeral=True)
    else:
        embed = discord.Embed(title='Вот, что нашлось по запросу:',
                              description=f'[Если картинка не прогрузилась, нажмите сюда]({result.image})',
                              color=0x9900ff)
        embed.set_image(url=result.image)
        await interaction.response.send_message(embed=embed)
