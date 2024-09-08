import discord
from discord.ext import commands, tasks
import pystyle
import os
import json
import platform
from pystyle import Center
import fade
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
TOKEN = config["token"]
ROLE_NAME = config["role_name"]
STATUS_PHRASE = config["status_phrase"]
GUILD_ID = config["guild_id"]
LOG_CHANNEL_ID = config["log_channel_id"]
mascular = '''
██╗   ██╗ █████╗ ███╗   ██╗██╗████████╗██╗   ██╗     ██████╗  ██████╗ ████████╗
██║   ██║██╔══██╗████╗  ██║██║╚══██╔══╝╚██╗ ██╔╝     ██╔══██╗██╔═══██╗╚══██╔══╝
██║   ██║███████║██╔██╗ ██║██║   ██║    ╚████╔╝█████╗██████╔╝██║   ██║   ██║   
╚██╗ ██╔╝██╔══██║██║╚██╗██║██║   ██║     ╚██╔╝ ╚════╝██╔══██╗██║   ██║   ██║   
 ╚████╔╝ ██║  ██║██║ ╚████║██║   ██║      ██║        ██████╔╝╚██████╔╝   ██║   
  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝      ╚═╝        ╚═════╝  ╚═════╝    ╚═╝   
'''
faded_text = fade.brazil(mascular)
faded_text1 = fade.brazil('Support Us By Giving Star On Repo | .gg/mascular')
def cls():
    # Check the operating system and clear the console accordingly
    if platform.system() == 'Windows':
        os.system('cls')  # Clear console on Windows
    else:
        os.system('clear')  # Clear console on Unix-like systems
        
@bot.event
async def on_ready():
    cls()
    print(Center.XCenter(faded_text))
    print(Center.XCenter(faded_text1))
    print(fade.brazil(f'Logged in as {bot.user}'))
    status_check_loop.start()  # Start the loop to monitor statuses

# Task that runs every 3 seconds
@tasks.loop(seconds=3)
async def status_check_loop():
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        return

    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    for member in guild.members:
        # Skip bot accounts
        if member.bot:
            continue

        role = discord.utils.get(guild.roles, name=ROLE_NAME)
        if not role:
            print(f"Role '{ROLE_NAME}' not found")
            return

        # Check if the user has a custom status with the required phrase
        if member.activity and isinstance(member.activity, discord.CustomActivity) and STATUS_PHRASE in member.activity.name:
            # If user doesn't have the role but their status contains the phrase, add the role
            if role not in member.roles:
                await member.add_roles(role)
                await log_channel.send(f"✅ | Role **{ROLE_NAME}** added to **{member.name}** for using the phrase **{STATUS_PHRASE}** in their status.")
        else:
            # If user has the role but doesn't have the phrase in their status, remove the role
            if role in member.roles:
                await member.remove_roles(role)
                await log_channel.send(f"❌ | Role **{ROLE_NAME}** removed from **{member.name}** as they no longer have the phrase **{STATUS_PHRASE}** in their status.")

# Ensure the loop is running only when the bot is ready
@status_check_loop.before_loop
async def before_status_check_loop():
    await bot.wait_until_ready()

bot.run(TOKEN)
