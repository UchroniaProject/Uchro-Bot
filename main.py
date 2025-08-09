#!/usr/bin/python

# Uchro-Bot, 2021-2025
# © Waynd_d (@waynd_d) and Bastien Choulans (@bastienclns)
# Free to use and modify for personal usages. No commercial uses allowed.

import discord
from discord.ext import commands
import asyncio
import utils.misc as misc


### CONFIGURATION

CONFIG = misc.load_config()

if CONFIG is None:
    print("Impossible de charger la configuration. Veuillez vérifier le fichier config.yml.")
    exit(1)
    
LOGO_PATH = "src/images/Logo_UchroProject.png"
DISCORD_TOKEN = CONFIG["DISCORD_TOKEN"]
PROJECT_NAME = CONFIG["PROJECT_NAME"]

print(discord.__version__)


### BOT REQUIREMENTS

intents = discord.Intents.all()
activity = discord.Game(CONFIG["ACTIVITY"])
bot = commands.Bot(command_prefix=CONFIG["BOT_PREFIX"], intents=intents, activity=activity)
bot.log_channel_id = CONFIG["LOG_CHANNEL_ID"]

### COGS
initial_extensions = [
    "cogs.bot_management",
    "cogs.miscellaneous"
]

#################
### LANCEMENT ###
#################
            
async def load_extensions():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            print(f"Impossible de charger l'extension {extension}: {e}")

if __name__ == '__main__':
    try:
        asyncio.run(load_extensions())
        bot.run(token=DISCORD_TOKEN)
    except discord.errors.LoginFailure as e:
        print(f"Erreur de connexion: {e}")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite: {e}")
