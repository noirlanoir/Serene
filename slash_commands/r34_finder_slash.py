import asyncio
from settings.config import settings
import discord
from discord.ext import commands
from rule34Py import rule34Py


async def _r34_finder(interaction: discord.Interaction, запрос: str):
    search = запрос
    await interaction.response.defer()
    await asyncio.sleep(1.5)
    if not interaction.channel.is_nsfw() is True:
        return await interaction.followup.send('`В данном канале не включен nsfw режим, включите его, для того чтобы использовать эту команду.`', ephemeral=True)
    r34Py = rule34Py()
    result = r34Py.random_post([f"{search}"])
    if str(result) == '[]':
        return await interaction.followup.send('`По вашему запросу ничего не найдено.`', ephemeral=True)
    else:
        embed = discord.Embed(title='Вот, что нашлось по запросу:', description=f'[Если картинка не прогрузилась, нажмите сюда]({result.image})', color=0x9900ff)
        embed.set_image(url=result.image)
        await interaction.followup.send(embed=embed)


