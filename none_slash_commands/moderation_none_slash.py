from datetime import datetime
from settings.config import settings
import discord
from discord.ext import commands
import json
import os

curr_dir = os.path.abspath(os.curdir)
project_dir = os.path.dirname(curr_dir)
prefix_dir = project_dir + '\settings\prefix.json'


def get_prefix(bot, message):
    with open(prefix_dir, 'r') as f:
        prefix = json.load(f)
    return prefix[str(message.guild.id)]


bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if interaction:
        return
    if error:
        return


@bot.command()
async def clear(ctx, amount: int):
    if not ctx.author.guild_permissions.manage_messages:
        return await ctx.send('`У вас отсутствуют права на это действие.`')
    if amount <= 0:
        return await ctx.send('Количество удаляемых сообщений должно быть больше 0.')
    if amount > 500:
        return await ctx.send('Очистить за раз можно не больше 500 сообщений.')
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f'Удалено `{len(deleted)}` сообщений.')


@bot.command()
async def unban(ctx, member_id: int):
    #     if not ctx.author.guild_permissions.administrator:
    #         return await ctx.send('`У вас отсутствуют права на это действие.`')
    global banned_user
    if member_id is None:
        embed_error = discord.Embed(title='Ошибка снятия бана.',
                                    description=f'{ctx.author.mention}, Укажите id пользователя!',
                                    color=0x9900ff)
        return await ctx.send(embed=embed_error)
    try:
        banned_user = await bot.fetch_user(member_id)
        await ctx.guild.unban(banned_user)
        await ctx.send(f'`Пользователь` {banned_user.mention} `был разбанен.`')
    except discord.errors.NotFound:
        embed_error = discord.Embed(title='Ошибка снятия бана.',
                                    description=f'{ctx.author.mention}, Пользователь не в бане!',
                                    color=0x9900ff)
        await ctx.reply(embed=embed_error)


@bot.event
async def on_command_error(ctx, error):
    if ctx.message.author is None:
        pass
    if isinstance(error, discord.ext.commands.CommandNotFound):
        pass


@bot.event
async def on_ready():
    print(bot.user, 'is ready')


bot.run(settings['token'])
