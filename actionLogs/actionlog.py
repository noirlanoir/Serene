from settings.config import settings
import discord
from discord import app_commands
from discord.ext import commands
from pymongo import MongoClient
from datetime import datetime, timedelta

bot = commands.Bot(command_prefix=settings['prefix'], case_insensitive=True, intents=discord.Intents.all())
bot.remove_command('help')
client = MongoClient(settings['database_url'])
database = client.SereneDB.DsActLog


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


@bot.event
async def on_ready():
    print('bot is ready')


@bot.event
async def on_member_remove(member):
    global kick, ban, got_ban
    isEnabled = database.find_one({'guild_id': member.guild.id})['enabled']
    isEnabledLeave = database.find_one({'guild_id': member.guild.id})['member_leave']
    logChannel = database.find_one({'guild_id': member.guild.id})['actlogchannel']
    isEnabledKick = database.find_one({'guild_id': member.guild.id})['member_kick']
    isEnabledBan = database.find_one({'guild_id': member.guild.id})['member_ban']
    server = bot.get_guild(member.guild.id)
    log_channel = server.get_channel(int(logChannel))
    if isEnabled == 'False':
        return
    if logChannel == '':
        return
    try:
        got_ban = await server.fetch_ban(member)
        if got_ban:
            if isEnabledBan == 'True':
                async for ban in server.audit_logs(action=discord.AuditLogAction.ban, limit=1):
                    print('\n')
                embed = discord.Embed(title='[BAN]', color=0x9900ff)
                embed.add_field(name='`Пользователь:`', value=ban.target.mention, inline=False)
                embed.add_field(name='Забанил:', value=ban.user.mention, inline=False)
                embed.add_field(name='`Время:`', value=f'**{ban.created_at.strftime("%d.%m.%Y, %H:%M:%S")}**')
                embed.set_author(icon_url=member.guild.icon, name=member.guild.name)
                embed.set_footer(text="🤍 • Serene.")
                try:
                    return await log_channel.send(embed=embed)
                except AttributeError:
                    return
    except discord.errors.NotFound as e:
        if e:
            async for kick in server.audit_logs(action=discord.AuditLogAction.kick, limit=1):
                print('\n')
            if kick:
                if kick.created_at.timestamp() + 5 >= datetime.now().timestamp() <= (
                        datetime.now() + timedelta(seconds=15)).timestamp():
                    if isEnabledKick == 'True':
                        embed = discord.Embed(title='[KICK]', color=0x9900ff)
                        embed.add_field(name='`Пользователь:`', value=kick.target.mention, inline=False)
                        embed.add_field(name='Кикнул:', value=kick.user.mention, inline=False)
                        embed.add_field(name='`Время:`', value=f'**{kick.created_at.strftime("%d.%m.%Y, %H:%M:%S")}**')
                        embed.set_author(icon_url=member.guild.icon, name=member.guild.name)
                        embed.set_footer(text="🤍 • Serene.")
                        try:
                            return await log_channel.send(embed=embed)
                        except AttributeError:
                            return
                else:
                    if isEnabledLeave == 'True':
                        embed = discord.Embed(title='[LEAVE]', color=0x9900ff)
                        embed.add_field(name='`Пользователь:`', value=member.mention, inline=False)
                        embed.add_field(name='`Время:`', value=f'**{datetime.now().strftime("%d.%m.%Y, %H:%M:%S")}**')
                        embed.set_author(icon_url=member.guild.icon, name=member.guild.name)
                        embed.set_footer(text="🤍 • Serene.")
                        try:
                            await log_channel.send(embed=embed)
                        except AttributeError:
                            return


@bot.event
async def on_member_join(member):
    isEnabled = database.find_one({'guild_id': member.guild.id})['enabled']
    logChannel = database.find_one({'guild_id': member.guild.id})['actlogchannel']
    isEnabledJoin = database.find_one({'guild_id': member.guild.id})['member_join']
    server = bot.get_guild(member.guild.id)
    log_channel = server.get_channel(int(logChannel))
    if isEnabled == 'False':
        return
    if logChannel == '':
        return
    if isEnabledJoin == 'True':
        embed = discord.Embed(title='[JOIN]', color=0x9900ff)
        embed.add_field(name='`Пользователь:`', value=member.mention, inline=False)
        embed.add_field(name='`Время:`', value=f'**{datetime.now().strftime("%d.%m.%Y, %H:%M:%S")}**')
        embed.set_author(icon_url=member.guild.icon, name=member.guild.name)
        embed.set_footer(text="🤍 • Serene.")
        try:
            await log_channel.send(embed=embed)
        except AttributeError:
            return


@bot.event
async def on_member_unban(guild, user):
    isEnabled = database.find_one({'guild_id': guild.id})['enabled']
    logChannel = database.find_one({'guild_id': guild.id})['actlogchannel']
    isEnabledMemberUnban = database.find_one({'guild_id': guild.id})['member_unban']
    server = bot.get_guild(guild.id)
    if isEnabled == 'False':
        return
    if logChannel == '':
        return
    log_channel = server.get_channel(int(logChannel))
    if isEnabledMemberUnban == 'False':
        return
    global entry
    if user is None:
        pass
    async for entry in guild.audit_logs(action=discord.AuditLogAction.unban, limit=1):
        print('\n')
    embed_unban = discord.Embed(color=0x9900ff,
                                title=f'`[UNBAN]`')
    embed_unban.add_field(name='`Пользователь:`', value=entry.user.mention, inline=False)
    embed_unban.add_field(name='`Разбанил:`', value=entry.target.mention, inline=False)
    embed_unban.add_field(name='`Время:`', value=f'**{datetime.now().strftime("%d.%m.%Y, %H:%M:%S")}**')
    embed_unban.set_author(icon_url=guild.icon, name=guild.name)
    embed_unban.set_footer(text="🤍 • Serene.")
    try:
        await log_channel.send(embed=embed_unban)
    except AttributeError:
        return


@bot.event
async def on_member_update(before, after):
    global member_update, roles_before, roles_after, update
    isEnabled = database.find_one({'guild_id': before.guild.id})['enabled']
    logChannel = database.find_one({'guild_id': before.guild.id})['actlogchannel']
    isEnabledUpdate = database.find_one({'guild_id': before.guild.id})['member_update']
    server = bot.get_guild(before.guild.id)
    if isEnabled == 'False':
        return
    if logChannel == '':
        return
    log_channel = server.get_channel(int(logChannel))
    if isEnabledUpdate == 'False':
        return
    async for member_update in server.audit_logs(action=discord.AuditLogAction.member_role_update, limit=1):
        print('\n')
    if member_update:
        roles_before = before.roles
        roles_after = after.roles
        if len(roles_before) < len(roles_after):
            new_role_given = next(role for role in after.roles if role not in before.roles)
            embed_role_given = discord.Embed(
                color=0x9900ff, title=f'`Выдача роли`',
                description=f"`Роли пользователя` <@{member_update.target.id}> `были изменены.`")
            embed_role_given.add_field(name='`Выдана роль:`', value=new_role_given.mention, inline=False)
            embed_role_given.add_field(name=f'`Выдал:`', value=member_update.user.mention, inline=False)
            embed_role_given.set_author(icon_url=before.guild.icon, name=before.guild.name)
            embed_role_given.set_footer(text="🤍 • Serene.")
            embed_role_given.timestamp = datetime.now()
            return await log_channel.send(embed=embed_role_given)
        if len(roles_before) > len(roles_after):
            role_taken = next(role for role in before.roles if role not in after.roles)
            embed_role_taken = discord.Embed(
                color=0x9900ff, title=f'`Снятие роли`',
                description=f"`Роли пользователя` <@{member_update.target.id}> `были изменены.`")
            embed_role_taken.add_field(name='`Снята роль:`', value=role_taken.mention, inline=False)
            embed_role_taken.add_field(name=f'`Снял:`', value=member_update.user.mention, inline=False)
            embed_role_taken.set_author(icon_url=before.guild.icon, name=before.guild.name)
            embed_role_taken.set_footer(text="🤍 • Serene.")
            embed_role_taken.timestamp = datetime.now()
            return await log_channel.send(embed=embed_role_taken)
    async for update in server.audit_logs(action=discord.AuditLogAction.member_update, limit=1):
        print('\n')
    if update:
        if update.user == update.target:
            pass
        else:
            if before.display_name == after.display_name:
                return
            embed_user_upd = discord.Embed(title='`Обновление пользователя`',
                                           description=f'`Пользователь` <@{update.user.id}> `сменил ник` <@{update.target.id}>`.`',
                                           color=0x9900ff
                                           )
            embed_user_upd.add_field(name='`Был:`', value=before.display_name, inline=False)
            embed_user_upd.add_field(name='`Стал:`', value=after.display_name, inline=False)
            embed_user_upd.set_author(icon_url=before.guild.icon, name=before.guild.name)
            embed_user_upd.set_footer(text="🤍 • Serene.")
            embed_user_upd.timestamp = datetime.now()
            try:
                return await log_channel.send(embed=embed_user_upd)
            except AttributeError:
                return
    name_before = before.display_name
    name_after = after.display_name
    if name_before == name_after:
        return
    else:
        embed_nickname_changed = discord.Embed(
            color=0x9900ff, title=f'`Смена никнейма`',
        )
        embed_nickname_changed.add_field(name='`Пользователь:`', value=before.mention)
        embed_nickname_changed.add_field(name='`Старый ник:`', value=name_before, inline=False)
        embed_nickname_changed.add_field(name='`Новый ник:`', value=name_after, inline=False)
        embed_nickname_changed.set_author(name=f"{server.name}", icon_url=server.icon)
        embed_nickname_changed.set_footer(text="🤍 • Serene.")
        embed_nickname_changed.timestamp = datetime.now()
        try:
            await log_channel.send(embed=embed_nickname_changed)
        except AttributeError:
            return


@bot.event
async def on_guild_channel_create(channel):
    isEnabled = database.find_one({'guild_id': channel.guild.id})['enabled']
    logChannel = database.find_one({'guild_id': channel.guild.id})['actlogchannel']
    isEnabledChannelCreate = database.find_one({'guild_id': channel.guild.id})['channel_create']
    server = bot.get_guild(channel.guild.id)
    if isEnabled == 'False':
        return
    if logChannel == '':
        return
    log_channel = server.get_channel(int(logChannel))
    if isEnabledChannelCreate == 'False':
        return
    global entry
    async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_create, limit=1):
        print('\n')
    embed_channel_create = discord.Embed(
        colour=0x9900ff,
        title='`Создание канала`',
    )
    embed_channel_create.add_field(name='`Создал:`', value=f'<@{entry.user.id}>')
    embed_channel_create.add_field(name='`Название канала: `', value=f'**{channel.name}**', inline=False)
    embed_channel_create.add_field(name='`Ссылка на канал: `', value=f'<#{entry.target.id}>', inline=False)
    embed_channel_create.set_author(name=f"{server.name}", icon_url=server.icon)
    embed_channel_create.set_footer(text="🤍 • Serene.")
    embed_channel_create.timestamp = datetime.now()
    try:
        await log_channel.send(embed=embed_channel_create)
    except AttributeError:
        return


@bot.event
async def on_guild_channel_delete(channel):
    isEnabled = database.find_one({'guild_id': channel.guild.id})['enabled']
    logChannel = database.find_one({'guild_id': channel.guild.id})['actlogchannel']
    isEnabledChannelDelete = database.find_one({'guild_id': channel.guild.id})['channel_delete']
    server = bot.get_guild(channel.guild.id)
    if isEnabled == 'False':
        return
    if logChannel == '':
        return
    log_channel = server.get_channel(int(logChannel))
    if isEnabledChannelDelete == 'False':
        return
    global entry
    async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1):
        print('\n')
    embed_channel_delete = discord.Embed(
        colour=0x9900ff,
        title='`Удаление канала`',
    )
    embed_channel_delete.add_field(name='`Удалил:`', value=entry.user.mention)
    embed_channel_delete.add_field(name='`Название канала: `', value=f'**{channel.name}**', inline=False)
    embed_channel_delete.set_author(name=f"{server.name}", icon_url=server.icon)
    embed_channel_delete.set_footer(text="🤍 • Serene.")
    embed_channel_delete.timestamp = datetime.now()
    try:
        await log_channel.send(embed=embed_channel_delete)
    except AttributeError:
        return


@bot.event
async def on_guild_channel_update(before, after):
    isEnabled = database.find_one({'guild_id': before.guild.id})['enabled']
    logChannel = database.find_one({'guild_id': before.guild.id})['actlogchannel']
    isEnabledChannelUpdate = database.find_one({'guild_id': before.guild.id})['channel_update']
    server = bot.get_guild(before.guild.id)
    if isEnabled == 'False':
        return
    if logChannel == '':
        return
    log_channel = server.get_channel(int(logChannel))
    if isEnabledChannelUpdate == 'False':
        return
    global entry
    before_name = before.name
    after_name = after.name
    if before_name == after_name:
        return
    async for entry in before.guild.audit_logs(action=discord.AuditLogAction.channel_update):
        print('\n')
    embed_channel_update = discord.Embed(
        title=f"`Переименование канала`",
        description=f"`Канал` <#{after.id}> `был переименован`",
        color=0x9900ff,
    )
    embed_channel_update.add_field(name='`Старое название:`', value=f'**{before_name}**', inline=False)
    embed_channel_update.add_field(name='`Новое название:`', value=f'**{after_name}**', inline=False)
    embed_channel_update.add_field(name='`Обновил:`', value=f'<@{entry.user.id}>')
    embed_channel_update.set_author(name=f"{server.name}", icon_url=server.icon)
    embed_channel_update.set_footer(text="🤍 • Serene.")
    embed_channel_update.timestamp = datetime.now()
    try:
        await log_channel.send(embed=embed_channel_update)
    except AttributeError:
        return


@bot.event
async def on_guild_role_update(before, after):
    isEnabled = database.find_one({'guild_id': before.guild.id})['enabled']
    logChannel = database.find_one({'guild_id': before.guild.id})['actlogchannel']
    isEnabledRoleUpdate = database.find_one({'guild_id': before.guild.id})['role_update']
    server = bot.get_guild(before.guild.id)
    if isEnabled == 'False':
        return
    if logChannel == '':
        return
    log_channel = server.get_channel(int(logChannel))
    if isEnabledRoleUpdate == 'False':
        return
    global entry
    colour_before = before.colour
    async for entry in before.guild.audit_logs(action=discord.AuditLogAction.role_update, limit=1):
        print('\n')
    colour_after = after.colour
    if before.name == after.name and colour_after != colour_before:
        embed_role_update = discord.Embed(
            title='`Обновление роли`',
            colour=0x9900ff,
            description="`У роли` " + before.mention + f' `изменен цвет`\n '
        )
        embed_role_update.add_field(name='`Старый цвет:`', value=f'**{colour_before}**', inline=False)
        embed_role_update.add_field(name='`Новый цвет:`', value=f'**{colour_after}**', inline=False)
        embed_role_update.add_field(name='`Обновил:`', value=f'<@{entry.user.id}>', inline=False)
        embed_role_update.set_footer(text="🤍 • Serene.")
        embed_role_update.set_author(name=f"{server.name}", icon_url=server.icon)
        embed_role_update.timestamp = datetime.now()
        try:
            await log_channel.send(embed=embed_role_update)
        except AttributeError:
            return
    if before.name != after.name:
        embed_role_update = discord.Embed(
            title='`Обновление роли`',
            colour=0x9900ff,
            description="`Роль` " + after.mention + "` переименована`\n"
        )
        embed_role_update.add_field(name='`Старое имя:`', value=f'**{before.name}**', inline=False)
        embed_role_update.add_field(name='`Новое имя:`', value=f'**{after.name}**', inline=False)
        embed_role_update.add_field(name='`Обновил:`', value=f'<@{entry.user.id}>', inline=False)
        embed_role_update.set_author(name=f"{server.name}", icon_url=server.icon)
        embed_role_update.set_footer(text="🤍 • Serene.")
        embed_role_update.timestamp = datetime.now()
        try:
            await log_channel.send(embed=embed_role_update)
        except AttributeError:
            return


@bot.event
async def on_guild_role_create(role):
    global entry
    isEnabled = database.find_one({'guild_id': role.guild.id})['enabled']
    logChannel = database.find_one({'guild_id': role.guild.id})['actlogchannel']
    isEnabledRoleUpdate = database.find_one({'guild_id': role.guild.id})['role_create']
    server = bot.get_guild(role.guild.id)
    if isEnabled == 'False':
        return
    if logChannel == '':
        return
    log_channel = server.get_channel(int(logChannel))
    if isEnabledRoleUpdate == 'False':
        return
    async for entry in role.guild.audit_logs(action=discord.AuditLogAction.role_delete, limit=1):
        print('\n')
    embed_role_create = discord.Embed(
        title=f"`Создание новой роли`",
        color=0x9900ff,
        timestamp=role.created_at)
    embed_role_create.add_field(name='`Название:`', value=f'**{role.name}**({role.mention})', inline=False)
    embed_role_create.add_field(name='`Создал:`', value=f'<@{entry.user.id}>', inline=False)
    embed_role_create.set_author(name=f"{server.name}", icon_url=server.icon)
    embed_role_create.set_footer(text="🤍 • Serene.")
    embed_role_create.timestamp = datetime.now()
    try:
        await log_channel.send(embed=embed_role_create)
    except AttributeError:
        return


@bot.event
async def on_guild_role_delete(role):
    isEnabled = database.find_one({'guild_id': role.guild.id})['enabled']
    logChannel = database.find_one({'guild_id': role.guild.id})['actlogchannel']
    isEnabledRoleUpdate = database.find_one({'guild_id': role.guild.id})['role_delete']
    server = bot.get_guild(role.guild.id)
    if isEnabled == 'False':
        return
    if logChannel == '':
        return
    log_channel = server.get_channel(int(logChannel))
    if isEnabledRoleUpdate == 'False':
        return
    global entry
    async for entry in role.guild.audit_logs(action=discord.AuditLogAction.role_delete, limit=1):
        print('\n')
    embed_role_delete = discord.Embed(
        title=f"`Удаление роли`",
        color=0x9900ff,
        timestamp=role.created_at)
    embed_role_delete.add_field(name='`Название:`', value=f'**{role}**', inline=False)
    embed_role_delete.add_field(name='`Удалил:`', value=f'<@{entry.user.id}>', inline=False)
    embed_role_delete.set_author(name=f"{server.name}", icon_url=server.icon)
    embed_role_delete.set_footer(text="🤍 • Serene.")
    embed_role_delete.timestamp = datetime.now()
    try:
        await log_channel.send(embed=embed_role_delete)
    except AttributeError:
        return


@bot.event
async def on_message_delete(message):
    isEnabled = database.find_one({'guild_id': message.guild.id})['enabled']
    logChannel = database.find_one({'guild_id': message.guild.id})['actlogchannel']
    isEnabledMessageDelete = database.find_one({'guild_id': message.guild.id})['message_delete']
    server = bot.get_guild(message.guild.id)
    if isEnabled == 'False':
        return
    if logChannel == '':
        return
    log_channel = server.get_channel(int(logChannel))
    if isEnabledMessageDelete == 'False':
        return
    message_sent_channel = message.channel
    try:
        img = message.attachments[0].proxy_url
        if message.content == '':
            embed_message_deleted_image = discord.Embed(title='`Удаленние картинки`',
                                                        colour=0xFF0000)
            embed_message_deleted_image.add_field(name='`Канал:`',
                                                  value=f"<#{message_sent_channel.id}>",
                                                  inline=False
                                                  )
            embed_message_deleted_image.add_field(name='`Автор:`', value=message.author.mention, inline=False)
            embed_message_deleted_image.set_image(url=img)
            embed_message_deleted_image.set_footer(text="🤍 • Serene.")
            embed_message_deleted_image.timestamp = datetime.now()
            try:
                await logChannel.send(embed=embed_message_deleted_image)
            except AttributeError:
                return
        if message.content != '':
            embed_message_deleted_image = discord.Embed(title='`Удаленние картинки`',
                                                        colour=0xFF0000)
            embed_message_deleted_image.add_field(name='`Сообщение с картинкой:`',
                                                  value=message.content,
                                                  inline=False
                                                  )
            embed_message_deleted_image.add_field(name='`Канал:`',
                                                  value=f"<#{message_sent_channel.id}>",
                                                  inline=False
                                                  )
            embed_message_deleted_image.add_field(name='`Автор:`', value=message.author.mention, inline=False)
            embed_message_deleted_image.set_image(url=img)
            embed_message_deleted_image.set_author(name=f"{server.name}", icon_url=server.icon)
            embed_message_deleted_image.set_footer(text="🤍 • Serene.")
            embed_message_deleted_image.timestamp = datetime.now()
            try:
                return await log_channel.send(embed=embed_message_deleted_image)
            except AttributeError:
                return
    except IndexError:
        pass
    if message.content == '':
        return
    embed_message_deleted = discord.Embed(
        title=f"`Сообщение было удалено`",
        color=0xFF0000)
    embed_message_deleted.add_field(
        name='`Удаленное сообщение:`', value=f"**{message.content}**",
        inline=False)
    embed_message_deleted.add_field(
        name='`Канал:`', value=f"<#{message_sent_channel.id}>",
        inline=False)
    embed_message_deleted.add_field(name='`Автор:`', value=message.author.mention, inline=False)
    embed_message_deleted.set_author(name=f"{server.name}", icon_url=server.icon)
    embed_message_deleted.set_footer(text="🤍 • Serene.")
    embed_message_deleted.timestamp = datetime.now()
    try:
        await log_channel.send(embed=embed_message_deleted)
    except AttributeError:
        return


@bot.event
async def on_message_edit(message_before, message_after):
    try:
        isEnabled = database.find_one({'guild_id': message_before.guild.id})['enabled']
    except AttributeError:
        return
    logChannel = database.find_one({'guild_id': message_before.guild.id})['actlogchannel']
    isEnabledMessageEdit = database.find_one({'guild_id': message_before.guild.id})['message_edit']
    server = bot.get_guild(message_before.guild.id)
    if isEnabled == 'False':
        return
    if logChannel == '':
        return
    log_channel = server.get_channel(int(logChannel))
    if isEnabledMessageEdit == 'False':
        return
    message_sent_channel_id = message_before.channel.id
    if message_before.content == message_after.content:
        return
    embed_message_edited = discord.Embed(
        title=f"`Сообщение было отредактировано`",
        color=0xFF0000)
    embed_message_edited.add_field(
        name='`Сообщение до редактирования:`', value=f"**{message_before.content}**",
        inline=False)
    embed_message_edited.add_field(
        name='`Сообщение после редактирования:`', value=f"**{message_after.content}**",
        inline=False)
    embed_message_edited.add_field(
        name='`Канал:`', value=f"<#{message_sent_channel_id}>",
        inline=False)
    embed_message_edited.add_field(name='`Автор:`', value=message_before.author.mention)
    embed_message_edited.set_author(name=f"{server.name}", icon_url=server.icon)
    embed_message_edited.set_footer(text="🤍 • Serene.")
    embed_message_edited.timestamp = datetime.now()
    try:
        await log_channel.send(embed=embed_message_edited)
    except AttributeError:
        return


@bot.event
async def on_voice_state_update(member, before, after):
    isEnabled = database.find_one({'guild_id': member.guild.id})['enabled']
    logChannel = database.find_one({'guild_id': member.guild.id})['actlogchannel']
    isEnabledVoiceUpdate = database.find_one({'guild_id': member.guild.id})['voice_update']
    server = bot.get_guild(member.guild.id)
    if isEnabled == 'False':
        return
    if logChannel == '':
        return
    log_channel = server.get_channel(int(logChannel))
    if isEnabledVoiceUpdate == 'False':
        return
    if before.channel is None and after.channel is not None:
        channel_id_join = member.voice.channel.id
        embed_join_voice = discord.Embed(
            color=0x9900ff, title=f'`Присоединение к голосовому каналу`',
            description=f'{member.mention} `Зашел в голосовой канал` <#{channel_id_join}>')
        embed_join_voice.set_author(name=f"{server.name}", icon_url=server.icon)
        embed_join_voice.set_footer(text="🤍 • Serene.")
        embed_join_voice.timestamp = datetime.now()
        try:
            await log_channel.send(embed=embed_join_voice)
        except AttributeError:
            return
    if before.channel is not None and after.channel is None:
        channel_id_leave = before.channel.id
        embed_leave_voice = discord.Embed(
            color=0x9900ff, title=f'`Выход из голосового канала`',
            description=f'{member.mention} `Вышел из голосового канала` <#{channel_id_leave}>')
        embed_leave_voice.set_author(name=f"{server.name}", icon_url=server.icon)
        embed_leave_voice.set_footer(text="🤍 • Serene.")
        embed_leave_voice.timestamp = datetime.now()
        try:
            await log_channel.send(embed=embed_leave_voice)
        except AttributeError:
            return
    if before.channel is not None and after.channel is not None and before.channel != after.channel:
        channel_id_switch_before = before.channel.id
        channel_id_switch_after = after.channel.id
        embed_channel_switched = discord.Embed(
            color=0x9900ff, title=f'`Смена голосового канала`',
            description=f'{member.mention} `Сменил голосовой канал:` <#{channel_id_switch_before}> `➡` <#{channel_id_switch_after}>')
        embed_channel_switched.set_author(name=f"{server.name}", icon_url=server.icon)
        embed_channel_switched.set_footer(text="🤍 • Serene.")
        embed_channel_switched.timestamp = datetime.now()
        try:
            await log_channel.send(embed=embed_channel_switched)
        except AttributeError:
            return


bot.run(settings['token'])
