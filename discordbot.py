# --------------------------------------------------------------
# Author: Cold Id-deen
# Date: 5/23/2025
# Purpose: Discord Moderation Bot for test purposes.
# This bot includes:
#   - Basic responses to messages ($hello, $who)
#   - Moderation commands: !kick, !ban, !unban, !banlist
#   - Reaction-based confirmation for kick/ban
#   - Logging of bans/unbans to a file on Desktop
#   - Unban using only username (no discriminator needed)
# Note: This is a test version, built for experimentation and
# learning, not production. Use responsibly.
# --------------------------------------------------------------

import discord
from discord.ext import commands
import asyncio
import os
from datetime import datetime

# Set up the required Discord bot intents
intents = discord.Intents.default()
intents.message_content = True  # To read message content
intents.reactions = True        # To track reaction responses

# Initialize the bot with command prefix "!" and the defined intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Path to the log file stored on the user's Desktop
log_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "ban_unban_log.txt")

def log_action(action_type, target_user, performed_by, reason=None):
    '''
    Logs moderation actions (BAN, UNBAN) to a text file on the Desktop.

    Parameters:
        action_type (str): Action type, e.g., "BAN" or "UNBAN"
        target_user (str): The user who was acted on, including ID
        performed_by (discord.User): Moderator who executed the command
        reason (str, optional): Reason for the action
    '''
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reason = reason if reason else "No reason provided"
    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {action_type}: {target_user} by {performed_by} | Reason: {reason}\n")

@bot.event
async def on_ready():
    '''
    Event: Called when the bot successfully connects to Discord.
    '''
    print(f'✅ Logged in as {bot.user}!')

@bot.event
async def on_message(message):
    '''
    Event: Called when a message is sent in a channel the bot can access.
    Handles $hello and $who. Also passes commands through to the bot.
    '''
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello World!')

    elif message.content.startswith('$who'):
        await message.channel.send(f'I am a bot for Cold. Nice to meet you, {message.author.mention}!')

    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    '''
    Command: !kick
    Prompts for confirmation and kicks a user from the server.
    
    Parameters:
        ctx (commands.Context): Command context
        member (discord.Member): The member to kick
        reason (str, optional): Optional reason
    '''
    confirm_msg = await ctx.send(
        f"{ctx.author.mention}, are you sure you want to kick {member.mention}? React with 👍 to confirm or ❌ to cancel."
    )
    await confirm_msg.add_reaction("👍")
    await confirm_msg.add_reaction("❌")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["👍", "❌"] and reaction.message.id == confirm_msg.id

    try:
        reaction, _ = await bot.wait_for("reaction_add", timeout=30.0, check=check)

        if str(reaction.emoji) == "👍":
            try:
                await member.kick(reason=reason)
                await ctx.send(f"{member.mention} has been kicked. Reason: {reason}")
            except discord.Forbidden:
                await ctx.send("❌ I don't have permission to kick this user.")
            except discord.HTTPException as e:
                await ctx.send(f"❌ Kick failed: {e}")
        else:
            await ctx.send("Kick cancelled.")
    except asyncio.TimeoutError:
        await ctx.send("No response. Kick cancelled.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    '''
    Command: !ban
    Prompts for confirmation and bans a user from the server.
    Logs the action to a file on the Desktop.

    Parameters:
        ctx (commands.Context): Command context
        member (discord.Member): The member to ban
        reason (str, optional): Optional reason
    '''
    confirm_msg = await ctx.send(
        f"{ctx.author.mention}, are you sure you want to **ban** {member.mention}? React with 👍 to confirm or ❌ to cancel."
    )
    await confirm_msg.add_reaction("👍")
    await confirm_msg.add_reaction("❌")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["👍", "❌"] and reaction.message.id == confirm_msg.id

    try:
        reaction, _ = await bot.wait_for("reaction_add", timeout=30.0, check=check)

        if str(reaction.emoji) == "👍":
            try:
                await member.ban(reason=reason)
                await ctx.send(f"{member.mention} has been **banned**. Reason: {reason}")
                log_action("BAN", f"{member} (ID: {member.id})", ctx.author, reason)
            except discord.Forbidden:
                await ctx.send("❌ I don't have permission to ban this user.")
            except discord.HTTPException as e:
                await ctx.send(f"❌ Ban failed: {e}")
        else:
            await ctx.send("Ban cancelled.")
    except asyncio.TimeoutError:
        await ctx.send("No response. Ban cancelled.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, username):
    '''
    Command: !unban
    Unbans a user by username (discriminator not required).
    Logs the action to a file on the Desktop.

    Parameters:
        ctx (commands.Context): Command context
        username (str): Username of the banned user (no # needed)
    '''
    async for ban_entry in ctx.guild.bans():
        user = ban_entry.user
        if user.name.lower() == username.lower():
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} has been unbanned.")
            log_action("UNBAN", f"{user} (ID: {user.id})", ctx.author)
            return

    await ctx.send(f"❌ Could not find a banned user named `{username}`.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def banlist(ctx):
    '''
    Command: !banlist
    Displays a list of all banned users and their reasons.

    Parameters:
        ctx (commands.Context): Command context
    '''
    bans = []
    async for ban_entry in ctx.guild.bans():
        bans.append(ban_entry)

    if not bans:
        await ctx.send("✅ No users are currently banned.")
        return

    msg = "**🔒 Banned Users:**\n"
    for ban in bans:
        user = ban.user
        reason = ban.reason if ban.reason else "No reason provided"
        msg += f"- {user.name}#{user.discriminator} (ID: {user.id}) — Reason: {reason}\n"

    if len(msg) > 2000:
        msg = msg[:1990] + "\n...List truncated."

    await ctx.send(msg)

# 🔐 Start the bot — replace with your actual token
bot.run('YOUR_BOT_TOKEN_HERE')
