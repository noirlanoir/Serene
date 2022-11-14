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
async def unban(ctx, member: discord.Member = None):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send('`У вас отсутствуют права на это действие.`')
    if member is None:
        embed_error = discord.Embed(title='Ошибка снятия бана.',
                                    description=f'{ctx.author.mention}, Укажите пользователя!',
                                    color=0x9900ff)
        return await ctx.send(embed=embed_error)
    try:
        banned_user = await bot.fetch_user(member.id)
        await ctx.guild.unban(banned_user)
    except discord.errors.NotFound as e:
        if e:
            embed_error = discord.Embed(title='Ошибка снятия бана.',
                                        description=f'{ctx.author.mention}, Пользователь не в бане!',
                                        color=0x9900ff)
            return await ctx.send(embed=embed_error)
    embed_unban = discord.Embed(title=f'**Снятие бана.**', color=0x9900ff)
    embed_unban.add_field(name='`Снял:`', value=ctx.author.mention, inline=False)
    embed_unban.add_field(name='`Пользователь:`', value=member.mention, inline=True)
    embed_unban.add_field(name='`ID пользователя:`', value=member.id, inline=False)
    embed_unban.set_footer(text=f'Дата: {times_start.strftime("%Y-%M-%d, %H:%M:%S")}')
    embed_unban.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
    await ctx.send(embed=embed_unban)


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
