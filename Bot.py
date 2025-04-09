#!/usr/bin/python

# Uchro-Bot, 2021-2025
# © Waynd_d (@Waynd_d#6037) and Bastien Choulans (@Bastien#2125)
# Free to use and modify for personal usages. No commercial uses allowed.

import discord
from discord.ext import commands

import random
import io
import os
import requests
import pytz
import emoji

from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor

print(discord.__version__)

DISCORD_BACKGROUND = HexColor("#36393F")  # Fond gris foncé Discord
TEXT_COLOR = HexColor("#FFFFFF")  # Texte blanc

timezone = pytz.timezone("Europe/Paris")

### STORAGE LOCATION, DATA EXTRACTION

global token
with open("data.txt", 'r') as file:
    lines = file.readlines()
    token = lines[1]
    log_channel_id = int(lines[7])
    archives_category = int(lines[10])

### BOT REQUIREMENTS

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='uc!',intents=intents)

activity = discord.Game("préparer une nouvelle Désuétude. (uc!help)")

URL_LOGO = "https://cdn.discordapp.com/attachments/1105818718518395020/1105860967218298920/Logo_V4_Uchronia.png"

### EMBED

#Validation
embed_val = discord.Embed(
        colour = discord.Colour.green()
    )
embed_val.set_footer(text = "Uchronia", icon_url = URL_LOGO)

### ON STARTUP

@bot.event
async def on_ready():
    # sends a message in shell
    print("Uchro-Bot, a bot created for the french roleplay Discord server Uchronia.\n© Waynd_d et Bastien Choulans, 2021-2025.\nCoded in Python, with discord.py librairies.\n\nThe bot is ready ! Would you care to get a Great Depression for the road ?")

    # sends a message in your log channel
    await bot.change_presence(status=discord.Status.online, activity=activity)
    embed_val.clear_fields()
    embed_val.add_field(name=f"Activation",value=f"Uchro-Bot a correctement été démarré.")
    await bot.get_channel(log_channel_id).send(embed=embed_val)

    # sends a nice GIF in your log channel
    if random.randint(0,50) == 25:
        await bot.get_channel(log_channel_id).send("https://tenor.com/view/atomic-nuke-j-robert-oppenheimer-destroyer-of-the-worlds-death-gif-15159234")

### COUNTRY CREATION

@bot.command(name="creation_pays", help="Crée les salons d'un pays. Utilise le format SIGLE Nom du pays.")
@discord.ext.commands.has_permissions(administrator=True)
async def creation_pays(ctx, *options):

    # options are what is following the command "creation_pays"
    # 1st option = country code/abreviation ; the rest is full country name
    abrev = options[0]

    nom_du_pays = options[1]
    for i in range(2,len(options)):
        nom_du_pays += " "+options[i]
    nom_du_pays += " (" + abrev + ")"

    guild = ctx.guild
    role = nom_du_pays
    authorized_role = await guild.create_role(name=role)

    permissions_privees = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        authorized_role: discord.PermissionOverwrite(read_messages=True)
    }
    permissions_publiques = {
        guild.default_role: discord.PermissionOverwrite(send_messages=False),
        authorized_role: discord.PermissionOverwrite(send_messages=True)
    }
    category = await guild.create_category(nom_du_pays, overwrites=permissions_publiques)


   # every country will get those channels,
    salons_prives = ["Discussions MJ", "Actions", "Recherches", "Production", "Opérations", "Logs"]

    await guild.create_text_channel(abrev+"-Communications", overwrites=permissions_publiques, category=category)
    for salon in salons_prives:
        await guild.create_text_channel(abrev+"-"+salon, overwrites=permissions_privees, category=category)

    embed_val.clear_fields()
    embed_val.set_footer(text=f"Création de pays")
    embed_val.add_field(name=f"Création du pays validée !",value=f"Le rôle, la catégorie et l'ensemble des salons ont été correctement configurés !")
    await ctx.send(embed=embed_val)


### COUNTRY DELETING

@bot.command(name="suppression_pays", help="Supprime les salons d'un pays")
@discord.ext.commands.has_permissions(administrator=True)
async def suppression_pays(ctx, *, nom_du_pays):

    guild = ctx.guild
    category = discord.utils.get(guild.categories, name=nom_du_pays)
    role = discord.utils.get(guild.roles, name = nom_du_pays)

    for channel in category.text_channels:
        await channel.delete()
    await role.delete()
    await category.delete()
    embed_val.clear_fields()
    embed_val.set_footer(text=f"Suppression de pays")
    embed_val.add_field(name=f"Suppression de pays terminée !",value=f"Le rôle, la catégorie et l'ensemble des salons ont été correctement supprimés !")
    await ctx.send(embed=embed_val)

### COUNTRY ARCHIVING

@bot.command(name="arch_pays", help="Archive les salons d'un pays")
@discord.ext.commands.has_permissions(administrator=True)
async def arch_pays(ctx, *, nom_du_pays):

    guild = ctx.guild
    category = discord.utils.get(guild.categories, name=nom_du_pays)
    cat_archives = discord.utils.get(guild.categories, name="Archives V4 #1")
    role = discord.utils.get(guild.roles, name = nom_du_pays)

    joueurs_du_pays = []
    for membre in guild.members :
        for role_teste in membre.roles:
            if role_teste.name == nom_du_pays:
                joueurs_du_pays.append(membre)

    for channel in category.text_channels:
        for membre in joueurs_du_pays:
            await channel.set_permissions(membre,read_messages=True,send_messages=False)
        await channel.edit(name=channel.name,topic="Archives V.4 du pays "+nom_du_pays)
        await channel.move(end=True,category=cat_archives)

    await role.delete()
    await category.delete()
    embed_val.clear_fields()
    embed_val.set_footer(text=f"Archivage de pays")
    embed_val.add_field(name=f"Archivage de pays terminé !",value=f"Le rôle et la catégorie ont été supprimés, et l'ensemble des salons ont été correctement archivés !")
    await ctx.send(embed=embed_val)

#Archivage au format PDF

async def generate_thread_archive(thread):
    return await generate_archive(thread, exclude_last=False)

async def generate_archive(channel, exclude_last=True):
    # Mainly done with ChatGPT. Thanks Chatty !
    category = channel.category.name if isinstance(channel, discord.TextChannel) and channel.category else "Sans catégorie"
    date_now = datetime.now(timezone).strftime("%d/%m/%Y - %H:%M:%S")

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y_position = height - 50

    # Fond du PDF
    c.setFillColor(DISCORD_BACKGROUND)
    c.rect(0, 0, width, height, fill=True, stroke=False)
    c.setFillColor(TEXT_COLOR)
    c.setFont("Helvetica", 12)

    # Titre de l'archive centré
    header_text = f"Archivage du salon [{channel.name}] issu de la catégorie [{category}] réalisé le [{date_now}]."
    max_width = width - 80
    words = header_text.split()
    current_line = ""
    lines = []
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if c.stringWidth(test_line, "Helvetica", 12) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    for line in lines:
        text_width = c.stringWidth(line, "Helvetica", 12)
        c.drawString((width - text_width) / 2, y_position, line)
        y_position -= 15

    y_position -= 15

    messages = [msg async for msg in channel.history(limit=None, oldest_first=True)]
    if exclude_last:
        messages = messages[:-1]

    last_author_name = None
    last_timestamp = None

    def check_page_space(y_position, lines_needed=1):
        if y_position - (15 * lines_needed) < 50:
            c.showPage()
            c.setFillColor(DISCORD_BACKGROUND)
            c.rect(0, 0, width, height, fill=True, stroke=False)
            c.setFillColor(TEXT_COLOR)
            c.setFont("Helvetica", 9)
            return height - 50
        return y_position

    def replace_emojis(text):
        return emoji.demojize(text, delimiters=(":", ":"))

    for message in messages:
        author = message.author
        author_name = message.webhook_id and message.author.name or author.display_name
        timestamp = message.created_at.astimezone(timezone).strftime('[%d/%m/%Y - %H:%M:%S]')
        content = replace_emojis(message.clean_content)

        new_message_group = author_name != last_author_name or (
            last_timestamp and (message.created_at - last_timestamp).total_seconds() > 300)

        if new_message_group:
            y_position -= 35
        else:
            y_position -= 25  # léger ajustement ici

        if message.thread:
            c.setFont("Helvetica-Oblique", 9)
            y_position = check_page_space(y_position)
            c.drawString(80, y_position, f"Ouverture du fil : {message.thread.name}")
            y_position -= 20

            buffer_fil_path = await generate_thread_archive(message.thread)
            await message.thread.send("Fil archivé :white_check_mark:")

        if new_message_group:
            avatar_url = author.avatar.url if hasattr(author, 'avatar') and author.avatar else getattr(author, 'default_avatar', None)
            if not avatar_url and hasattr(author, 'avatar_url'):
                avatar_url = author.avatar_url
            if avatar_url:
                try:
                    response = requests.get(avatar_url)
                    avatar_img = ImageReader(io.BytesIO(response.content))
                    c.drawImage(avatar_img, 40, y_position - 5, width=30, height=30, mask='auto')
                except Exception as e:
                    print("Erreur avatar :", e)

            c.setFont("Helvetica-Bold", 10)
            name_width = c.stringWidth(author_name, "Helvetica-Bold", 10)
            y_position = check_page_space(y_position)
            c.drawString(80, y_position + 10, f"{author_name}")
            c.setFont("Helvetica-Oblique", 8)
            c.drawString(85 + name_width, y_position + 10, timestamp)
            y_position -= 3

        c.setFont("Helvetica", 9)

        wrapped_lines = []
        max_width_text = width - 100
        for line in content.split('\n'):
            words = line.split()
            current_line = ""
            for word in words:
                test_line = f"{current_line} {word}".strip()
                if c.stringWidth(test_line, "Helvetica", 9) <= max_width_text:
                    current_line = test_line
                else:
                    wrapped_lines.append(current_line)
                    current_line = word
            if current_line:
                wrapped_lines.append(current_line)

        for line in wrapped_lines:
            y_position = check_page_space(y_position)
            c.setFont("Helvetica", 9)
            c.drawString(80, y_position, line)
            y_position -= 10

        if message.attachments:
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif"]):
                    try:
                        img_response = requests.get(attachment.url)
                        img_reader = ImageReader(io.BytesIO(img_response.content))
                        img_width, img_height = img_reader.getSize()
                        aspect_ratio = img_width / img_height
                        display_width = 200
                        display_height = display_width / aspect_ratio
                        y_position -= display_height - 5
                        y_position = check_page_space(y_position)
                        c.drawImage(img_reader, 80, y_position, width=display_width, height=display_height, mask='auto')
                        y_position -= 10
                    except Exception as e:
                        print("Erreur chargement image :", e)
                else:
                    c.setFont("Helvetica-Oblique", 9)
                    file_text = f"[Fichier joint : {attachment.filename}] {attachment.url}"
                    file_lines = []
                    current_line = ""
                    for word in file_text.split():
                        test_line = f"{current_line} {word}".strip()
                        if c.stringWidth(test_line, "Helvetica-Oblique", 9) <= (width - 100):
                            current_line = test_line
                        else:
                            file_lines.append(current_line)
                            current_line = word
                    if current_line:
                        file_lines.append(current_line)
                    for line in file_lines:
                        y_position = check_page_space(y_position)
                        c.setFont("Helvetica-Oblique", 9)
                        c.drawString(80, y_position, line)
                        y_position -= 10

        y_position = check_page_space(y_position)
        last_author_name = author_name
        last_timestamp = message.created_at

    c.save()
    buffer.seek(0)

    if isinstance(channel, discord.Thread):
        category = channel.parent.category.name if channel.parent and channel.parent.category else "Sans catégorie"
        parent_name = channel.parent.name if channel.parent else "Salon inconnu"
        filename = f"Archive_{category}_{parent_name}_{channel.name}.pdf"
    else:
        filename = f"Archive_{category}_{channel.name}.pdf"

    with open(filename, "wb") as f:
        f.write(buffer.getbuffer())
    return filename

@bot.command(name="archive_pdf")
@discord.ext.commands.has_permissions(administrator=True)
async def archive_channel(ctx, *, target: str = None):
    if target:
        category = discord.utils.get(ctx.guild.categories, name=target)
        if category:
            for channel in category.text_channels:
                filepath = await generate_archive(channel)
                #await channel.send("Salon archivé :white_check_mark:")
            return
        channel = discord.utils.get(ctx.guild.text_channels, mention=target) or discord.utils.get(ctx.guild.text_channels, name=target)
    else:
        channel = ctx.channel

    if channel:
        filepath = await generate_archive(channel)
        #await channel.send("Salon archivé :white_check_mark:")
    else:
        await ctx.send("Salon ou catégorie introuvable.")

"""
async def fetch_image(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.read()
    except Exception as e:
        print(f"Erreur téléchargement image : {e}")
    return None

def generate_pdf_sync(channel, messages, category, date_now):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y_position = height - 50

    c.setFillColor(DISCORD_BACKGROUND)
    c.rect(0, 0, width, height, fill=True, stroke=False)
    c.setFillColor(TEXT_COLOR)
    c.setFont("Helvetica", 12)

    header_text = f"Archivage du salon [{channel.name}] issu de la catégorie [{category}] réalisé le [{date_now}]."
    max_width = width - 80
    words = header_text.split()
    current_line = ""
    lines = []
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if c.stringWidth(test_line, "Helvetica", 12) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    for line in lines:
        text_width = c.stringWidth(line, "Helvetica", 12)
        c.drawString((width - text_width) / 2, y_position, line)
        y_position -= 15

    y_position -= 15

    last_author_name = None
    last_timestamp = None

    def check_page_space(y_position, lines_needed=1):
        if y_position - (15 * lines_needed) < 50:
            c.showPage()
            c.setFillColor(DISCORD_BACKGROUND)
            c.rect(0, 0, width, height, fill=True, stroke=False)
            c.setFillColor(TEXT_COLOR)
            c.setFont("Helvetica", 9)
            return height - 50
        return y_position

    def replace_emojis(text):
        return emoji.demojize(text, delimiters=(":", ":"))

    for message in messages:
        author = message.author
        author_name = message.webhook_id and message.author.name or author.display_name
        timestamp = message.created_at.astimezone(timezone).strftime('[%d/%m/%Y - %H:%M:%S]')
        content = replace_emojis(message.clean_content)

        new_message_group = author_name != last_author_name or (
            last_timestamp and (message.created_at - last_timestamp).total_seconds() > 300)

        if new_message_group:
            y_position -= 35
        else:
            y_position -= 25

        if new_message_group:
            avatar_url = author.avatar.url if hasattr(author, 'avatar') and author.avatar else getattr(author, 'default_avatar', None)
            if not avatar_url and hasattr(author, 'avatar_url'):
                avatar_url = author.avatar_url
            if avatar_url:
                image_data = asyncio.run(fetch_image(avatar_url))
                if image_data:
                    try:
                        avatar_img = ImageReader(io.BytesIO(image_data))
                        c.drawImage(avatar_img, 40, y_position - 5, width=30, height=30, mask='auto')
                    except Exception as e:
                        print("Erreur avatar :", e)

            c.setFont("Helvetica-Bold", 10)
            name_width = c.stringWidth(author_name, "Helvetica-Bold", 10)
            y_position = check_page_space(y_position)
            c.drawString(80, y_position + 10, f"{author_name}")
            c.setFont("Helvetica-Oblique", 8)
            c.drawString(85 + name_width, y_position + 10, timestamp)
            y_position -= 3

        c.setFont("Helvetica", 9)
        wrapped_lines = []
        max_width_text = width - 100
        for line in content.split('\n'):
            words = line.split()
            current_line = ""
            for word in words:
                test_line = f"{current_line} {word}".strip()
                if c.stringWidth(test_line, "Helvetica", 9) <= max_width_text:
                    current_line = test_line
                else:
                    wrapped_lines.append(current_line)
                    current_line = word
            if current_line:
                wrapped_lines.append(current_line)

        for line in wrapped_lines:
            y_position = check_page_space(y_position)
            c.setFont("Helvetica", 9)
            c.drawString(80, y_position, line)
            y_position -= 10

        y_position = check_page_space(y_position)
        last_author_name = author_name
        last_timestamp = message.created_at

    c.save()
    buffer.seek(0)

    if isinstance(channel, discord.Thread):
        category = channel.parent.category.name if channel.parent and channel.parent.category else "Sans catégorie"
        parent_name = channel.parent.name if channel.parent else "Salon inconnu"
        filename = f"Archive_{category}_{parent_name}_{channel.name}.pdf"
    else:
        filename = f"Archive_{category}_{channel.name}.pdf"

    with open(filename, "wb") as f:
        f.write(buffer.getbuffer())
    return filename

async def generate_archive(channel, exclude_last=True):
    category = channel.category.name if isinstance(channel, discord.TextChannel) and channel.category else "Sans catégorie"
    date_now = datetime.now(timezone).strftime("%d/%m/%Y - %H:%M:%S")
    messages = [msg async for msg in channel.history(limit=None, oldest_first=True)]
    if exclude_last:
        messages = messages[:-1]
    return await asyncio.to_thread(generate_pdf_sync, channel, messages, category, date_now)

@bot.command(name="archive_pdf")
async def archive_channel(ctx, *, target: str = None):
    if target:
        category = discord.utils.get(ctx.guild.categories, name=target)
        if category:
            for channel in category.text_channels:
                filepath = await generate_archive(channel)
                await channel.send("Salon archivé :white_check_mark:")
            return
        channel = discord.utils.get(ctx.guild.text_channels, mention=target) or discord.utils.get(ctx.guild.text_channels, name=target)
    else:
        channel = ctx.channel

    if channel:
        filepath = await generate_archive(channel)
        await channel.send("Salon archivé :white_check_mark:")
    else:
        await ctx.send("Salon ou catégorie introuvable.")
"""


### ROLL

@bot.command(name="roll", help="Réalise un lancer de dé au hasard")
async def roll(ctx, tirage):
    """
    Drawing following the pattern "1d100+5", where 1 represents the number of throws,
    100 represents the value of the die, and 5 represents the value added to each independent throw.
    """
    try:
        nb_tirage = tirage.split("d")[0]

        if "+" in tirage:
            valeur_tirage = tirage.split("d")[1].split("+")[0]
            ajout = int(tirage.split("d")[1].split("+")[1])

        elif "-" in tirage:
            valeur_tirage = tirage.split("d")[1].split("-")[0]
            ajout = -int(tirage.split("d")[1].split("-")[1])

        else:
            valeur_tirage = tirage.split("d")[1]
            ajout = 0

        resultats_tirage = [random.randint(1, int(valeur_tirage)) for i in range(int(nb_tirage))]
        reponse = ""
        if len(resultats_tirage) > 1:
            reponse += f"Total: {sum(resultats_tirage) + ajout * len(resultats_tirage)}\n"
        reponse += "`"
        if ajout < 0:
            #If there is an addition, it is precised in the answer
            for element in resultats_tirage:
                reponse += f"{element+ajout} ({element} - {-ajout})  |  "
        elif ajout > 0:
            for element in resultats_tirage:
                reponse += f"{element+ajout} ({element} + {ajout})  |  "
        else:
            #Else, only the result is given
            for element in resultats_tirage:
                reponse += f"{element}  |  "

        #Deleting of the last "|"
        reponse = reponse[0:-5] + "`"
    except:
        raise Exception
    embed_tempo = discord.Embed(colour = discord.Colour.blue(), title = "Jet de dé 🎲")
    embed_tempo.add_field(name=f"Résultat",value=reponse)
    await ctx.send(embed=embed_tempo)


### ONLINE, OFFLINE, SHUTDOWN

# Offline

@bot.command(name="offline", help="Affiche le bot hors-ligne")
@discord.ext.commands.has_permissions(administrator=True)
async def offline(ctx):
    await bot.change_presence(status=discord.Status.offline, activity=None)
    await ctx.send("Non, attendez ! Ne m'éteignez pas ! Vous n'avez... pas... enc... ore... tout... vu... *le bot s'est éteint*")

# Online

@bot.command(name="online", help="Affiche le bot en ligne")
@discord.ext.commands.has_permissions(administrator=True)
async def online(ctx):
    await bot.change_presence(status=discord.Status.online, activity=activity)
    await ctx.send("*s'allume* Merci d'avoir choisi Uchro-Bot pour détruire Nolara.")

# Shutdown

@bot.command(name="shutdown", help="Eteint le bot")
@discord.ext.commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await bot.change_presence(status=discord.Status.offline, activity=None)
    embed_error = discord.Embed(colour = discord.Colour.red())
    embed_error.set_footer(text = "Uchronia", icon_url = URL_LOGO)
    embed_error.add_field(name=f"*Bip bip bip*",value=f"Uchro-Bot s'est correctement éteint.")
    await bot.get_channel(log_channel_id).send(embed=embed_error)
    await ctx.bot.close()


### MISC

# Ping
@bot.command(name="ping", help="Renvoie la latence du bot")
async def ping(ctx):
    embed_rep = discord.Embed(colour = discord.Colour.blue())
    embed_rep.set_footer(text = "Uchronia", icon_url = URL_LOGO)
    embed_rep.add_field(name=f"Pong !",value=f"Latence de {round(bot.latency * 1000)} ms")
    await ctx.send(embed=embed_rep)

#Wide
@bot.command(name="wide", help="Mystère !")
@discord.ext.commands.has_permissions(administrator=True)
async def wide(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/537667794112610314/1084138741670625511/Wide2.mp4")

#Brain_power
@bot.command(name="brain_power", help="Mystère !")
@discord.ext.commands.has_permissions(administrator=True)
async def brain_power(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/1105818718518395020/1122980909453410364/Brain_Power.mp4")

#president
@bot.command(name="president", help="Mystère !")
@discord.ext.commands.has_permissions(administrator=True)
async def president(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/1105818718518395020/1123715876202483792/CHIRAC_-_Je_serai_le_president_de_tous_les_Francais_samba_remix_.mp4")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("Commande inconnue.")
    elif isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send("Vous ne disposez pas des permissions requises.")
    else:
        await ctx.send("Erreur inconnue. Contactez un administrateur.")

#################
### LANCEMENT ###
#################

bot.run(token)
