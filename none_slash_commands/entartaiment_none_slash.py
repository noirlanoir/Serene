from datetime import datetime
from settings.config import settings
import discord
import json
from discord.ext import commands
import os

curr_dir = os.path.abspath(os.curdir)
project_dir = os.path.dirname(curr_dir)
prefix_dir = project_dir + '\settings\prefix.json'


def get_prefix(bot, message):
    with open(prefix_dir, 'r') as f:
        prefix = json.load(f)
    return prefix[str(message.guild.id)]


bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())


@bot.event
async def on_command_error(ctx, error):
    if ctx.message.author is None:
        pass
    if isinstance(error, discord.ext.commands.CommandNotFound):
        pass


@bot.command()
async def info(ctx, member: discord.Member = None):
    if member is None:
        mobile_status = ctx.author.mobile_status
        pc_status = ctx.author.desktop_status
        web_status = ctx.author.web_status
        if str(web_status) == 'offline':
            web_status_emoji = '🔴 `Не в сети`'
        else:
            web_status_emoji = '🟢 `В сети`'
        if str(pc_status) == 'offline':
            desc_status_emoji = '🔴 `Не в сети`'
        else:
            desc_status_emoji = '🟢 `В сети`'
        if str(mobile_status) == 'offline':
            mobile_status_emoji = '🔴 `Не в сети`'
        else:
            mobile_status_emoji = '`🟢 В сети`'
        roles = [r.mention for r in ctx.author.roles if r != ctx.guild.default_role]
        rolelist = "\n ".join(roles)
        if rolelist == '':
            rolelist = 'Роли отсутствуют.'
        author_status = ctx.author.status
        if str(author_status) == 'online':
            author_status = '`В сети.`'
        elif str(author_status) == 'idle':
            author_status = '`Неактивен.`'
        elif str(author_status) == 'dnd':
            author_status = '`Не беспокоить.`'
        else:
            author_status = '`Не в сети.`'
        embed = discord.Embed(color=0x9900ff, title=f'Информация о пользователе: {ctx.author.name}')
        embed.add_field(name='❖ Имя:', value='`' + ctx.author.name + '`')
        embed.add_field(name='❖ Имя на сервере:', value='`' + ctx.author.display_name + '`', inline=False)
        embed.add_field(name='❖ Айди:', value=f'`{ctx.author.id}`', inline=False)
        embed.add_field(name='❖ Аккаунт создан:',
                        value=f'`{ctx.author.created_at.strftime("%d.%m.%Y, %H:%M:%S")}`', inline=False)
        embed.add_field(name='❖ Количество ролей:', value=f'`{len(ctx.author.roles) - 1}`', inline=False)
        embed.add_field(name='❖ Роли:', value=f'\n{rolelist}', inline=False)
        embed.add_field(name='❖ Статус:', value=author_status)
        embed.add_field(name='❖ Статусы: ',
                        value=f'📱 Мобильный статус: {mobile_status_emoji}\n 🌍 Веб статус: {web_status_emoji}\n 💻 Пк статус: {desc_status_emoji}',
                        inline=False)
        embed.set_footer(text="🤍 • Serene.")
        await ctx.send(embed=embed)
    if member:
        mobile_status = member.mobile_status
        pc_status = member.desktop_status
        web_status = member.web_status
        if str(web_status) == 'offline':
            web_status_emoji = '🔴 `Не в сети`'
        else:
            web_status_emoji = '🟢 `В сети`'
        if str(pc_status) == 'offline':
            desc_status_emoji = '🔴 `Не в сети`'
        else:
            desc_status_emoji = '🟢 `В сети`'
        if str(mobile_status) == 'offline':
            mobile_status_emoji = '🔴 `Не в сети`'
        else:
            mobile_status_emoji = '`🟢 В сети`'
        roles = [r.mention for r in member.roles if r != ctx.guild.default_role]
        rolelist = "\n ".join(roles)
        if rolelist == '':
            rolelist = 'Роли отсутствуют.'
        member_status = member.status
        if str(member_status) == 'online':
            member_status = '`В сети.`'
        elif str(member_status) == 'idle':
            member_status = '`Неактивен.`'
        elif str(member_status) == 'dnd':
            member_status = '`Не беспокоить.`'
        else:
            member_status = '`Не в сети.`'
        embed = discord.Embed(color=0x9900ff, title=f'Информация о пользователе: {member.name}')
        embed.add_field(name='❖ Имя:', value='`' + member.name + '`')
        embed.add_field(name='❖ Имя на сервере:', value='`' + member.display_name + '`', inline=False)
        embed.add_field(name='❖ Айди:', value=f'`{member.id}`', inline=False)
        embed.add_field(name='❖ Аккаунт создан:',
                        value=f'`{member.created_at.strftime("%d.%m.%Y, %H:%M:%S")}`', inline=False)
        embed.add_field(name='❖ Количество ролей:', value=f'`{len(member.roles) - 1}`', inline=False)
        embed.add_field(name='❖ Роли:', value=f'\n{rolelist}', inline=False)
        embed.add_field(name='❖ Статус:', value=member_status)
        embed.add_field(name='❖ Статусы устройств: ',
                        value=f'📱 Мобильный статус: {mobile_status_emoji}\n 🌍 Веб статус: {web_status_emoji}\n 💻 Пк статус: {desc_status_emoji}',
                        inline=False)
        embed.set_footer(text="🤍 • Serene.")
        await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print(bot.user, 'is ready')


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if interaction:
        return
    if error:
        return


bot.run(settings['token'])
