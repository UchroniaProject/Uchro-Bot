# Uchro-Bot, 2021-2023
# © Waynd_d (@Waynd_d#6037) and Bastien Choulans (@Bastien#2125)
# Free to use and modify for personal usages. No commercial uses allowed.

import discord
from discord.ext import commands
import random
import os

print(discord.__version__)

### STORAGE LOCATION, DATA EXTRACTION

#location = input("Please indicate the location where all files are stored :")
#os.chdir(location)

global token
with open("data.txt", 'r') as file:
    lines = file.readlines()
    token = lines[1]
    log_channel_id = int(lines[7])
    archives_category = int(lines[10])

### BOT REQUIREMENTS

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='uc!',intents=intents)

activity = discord.Game("préparer une nouvelle Désuétude")

URL_LOGO = "https://cdn.discordapp.com/attachments/1105818718518395020/1105860967218298920/Logo_V4_Uchronia.png"

### PERMISSIONS ERROR EMBED

def erreur_permissions():
    embed_error.clear_fields()
    embed_error.set_footer(text=f"Erreur")
    embed_error.add_field(name=f"Désolé !",value=f"Il semblerait que vous ne disposez pas des permissions nécessaires à l'exécution de cette commande. Contactez un maître de jeu si vous pensez rencontrer une erreur.")
    return embed_error

# Answer
embed_rep = discord.Embed(
        colour = discord.Colour.blue()
    )
embed_rep.set_footer(text = "Uchronia", icon_url = URL_LOGO)

#Error
embed_error = discord.Embed(
        colour = discord.Colour.red()
    )
embed_error.set_footer(text = "Uchronia", icon_url = URL_LOGO)

#Validation
embed_val = discord.Embed(
        colour = discord.Colour.green()
    )
embed_val.set_footer(text = "Uchronia", icon_url = URL_LOGO)

### ON STARTUP

@bot.event
async def on_ready():
    # sends a message in shell
    print("Uchro-Bot, a bot created for the french roleplay Discord server Uchronia.\n© Waynd_d et Bastien Choulans, 2021-2023.\nCoded in Python, with discord.py librairies.\n\nThe bot is ready ! Would you care to get a Great Depression for the road ?")

    # sends a message in your log channel
    await bot.change_presence(status=discord.Status.online, activity=activity)
    embed_val.clear_fields()
    embed_val.add_field(name=f"Activation",value=f"Uchro-Bot a correctement été démarré.")
    await bot.get_channel(log_channel_id).send(embed=embed_val)

    # sends a nice GIF in your log channel
    if random.randint(0,50) == 25:
        await bot.get_channel(log_channel_id).send("https://tenor.com/view/atomic-nuke-j-robert-oppenheimer-destroyer-of-the-worlds-death-gif-15159234")

### COUNTRY CREATION

@bot.command(name="creation_pays", help="Crée les salons d'un pays")
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
    salons_prives = ["Discussions MJ", "Actions", "Recherches", "Production", "Opérations militaires", "Logs"]

    await guild.create_text_channel(abrev+"-Communications", overwrites=permissions_publiques, category=category)
    for salon in salons_prives:
        await guild.create_text_channel(abrev+"-"+salon, overwrites=permissions_privees, category=category)

    embed_val.clear_fields()
    embed_val.set_footer(text=f"Création de pays")
    embed_val.add_field(name=f"Création du pays validée !",value=f"Le rôle, la catégorie et l'ensemble des salons ont été correctement configurés !")
    await ctx.send(embed=embed_val)

@creation_pays.error
async def creation_pays_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(embed=erreur_permissions())

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

@suppression_pays.error
async def suppression_pays_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(embed=erreur_permissions())

### COUNTRY ARCHIVING

@bot.command(name="arch_pays", help="Archive les salons d'un pays")
@discord.ext.commands.has_permissions(administrator=True)
async def arch_pays(ctx, *, nom_du_pays):

    guild = ctx.guild
    category = discord.utils.get(guild.categories, name=nom_du_pays)
    cat_archives = discord.utils.get(guild.categories, id=arc)
    role = discord.utils.get(guild.roles, name = nom_du_pays)

    joueurs_du_pays = []
    for membre in guild.members :
        for role_teste in membre.roles:
            if role_teste.name == nom_du_pays:
                joueurs_du_pays.append(membre)

    for channel in category.text_channels:
        for membre in joueurs_du_pays:
            await channel.set_permissions(membre,read_messages=True,send_messages=False)
        nom_original = channel.name
        await channel.edit(name=abrev+"-"+channel.name,topic="Archives V.3005 du pays "+nom_du_pays)
        await channel.move(end=True,category=cat_archives)

    await role.delete()
    await category.delete()
    embed_val.clear_fields()
    embed_val.set_footer(text=f"Archivage de pays")
    embed_val.add_field(name=f"Archivage de pays terminé !",value=f"Le rôle et la catégorie ont été supprimés, et l'ensemble des salons ont été correctement archivés !")
    await ctx.send(embed=embed_val)

@arch_pays.error
async def arch_pays_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(embed=erreur_permissions())

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

    embed_rep.clear_fields()
    embed_rep.add_field(name=f"Jet de dé 🎲",value=reponse)
    await ctx.send(embed=embed_rep)

@roll.error
async def creation_pays_error(ctx):
    embed_error.clear_fields()
    embed_error.set_footer(text=f"Erreur")
    embed_error.add_field(name=f"Désolé !",value=f"Votre lancer de dé n'a pas été reconnu. Contactez un maître de jeu si vous pensez rencontrer une erreur.")
    await ctx.send(embed = embed_error)


### ONLINE, OFFLINE, SHUTDOWN

# Offline

@bot.command(name="offline", help="Affiche le bot hors-ligne")
@discord.ext.commands.has_permissions(administrator=True)
async def offline(ctx):
    await bot.change_presence(status=discord.Status.offline, activity=None)
    await ctx.send("Non, attendez ! Ne m'éteignez pas ! Vous n'avez... pas... enc... ore... tout... vu... *le bot s'est éteint*")

@offline.error
async def offline_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(embed=erreur_permissions())

# Online

@bot.command(name="online", help="Affiche le bot en ligne")
@discord.ext.commands.has_permissions(administrator=True)
async def online(ctx):
    await bot.change_presence(status=discord.Status.online, activity=activity)
    await ctx.send("*s'allume* Merci d'avoir choisi Uchro-Bot pour détruire Nolara.")

@online.error
async def online_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(embed=erreur_permissions())

# Shutdown

@bot.command(name="shutdown", help="Eteint le bot")
@discord.ext.commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await bot.change_presence(status=discord.Status.offline, activity=None)
    embed_error.clear_fields()
    embed_error.add_field(name=f"*Bip bip bip*",value=f"Uchro-Bot s'est correctement éteint.")
    await bot.get_channel(log_channel_id).send(embed=embed_error)
    await ctx.bot.close()

@shutdown.error
async def shutdown_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(embed=erreur_permissions())

### MISC

# Ping
@bot.command(name="ping", help="Renvoie la latence du bot")
async def ping(ctx):
    embed_rep.clear_fields()
    embed_rep.add_field(name=f"Pong !",value=f"Latence de {round(bot.latency * 1000)} ms")
    await ctx.send(embed=embed_rep)

# Smash ball
@bot.command(name="smash", help="Mystère !")
async def smash(ctx):
    await ctx.send("https://tenor.com/view/shaq-final-smash-satisfied-surprised-super-smash-bros-gif-17647942")

# The bot will copy the message sent by the user, precising who used the command
@bot.command(name="copy", help="Copie (dans un embed) le message envoyé par l'utilisateur après la commande, en précisant l'utilisateur")
async def copy(ctx, *, message):
    await ctx.message.delete()
    embed_rep.clear_fields()
    embed_rep.set_footer(text = f"{ctx.author.name}#{ctx.author.discriminator}", icon_url = ctx.author.avatar_url)
    embed_rep.add_field(name=f"Uchro-Bot",value = message)
    await ctx.send(embed=embed_rep)
    embed_rep.set_footer(text = "", icon_url = "")

# The bot will copy the same message sent by the user, without precising who used it (Administrator only)
@bot.command(name="copy_admin", help="Copie (dans un embed) le message envoyé par l'utilisateur après la commande, sans préciser l'utilisateur")
@discord.ext.commands.has_permissions(administrator=True)
async def copy_admin(ctx, *, message):
    await ctx.message.delete()
    embed_rep.clear_fields()
    embed_rep.add_field(name=f"Uchro-Bot", value = message)
    await ctx.send(embed=embed_rep)

@copy_admin.error
async def copy_admin_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(embed=erreur_permissions())

@bot.command(name="meteo", help="Affiche une météo au hasard")
async def meteo(ctx):
    correspondance = {"Calme": ":sunny:", "Pluvieux": ":cloud_rain:", "Venteux": ":wind_blowing_face:", "Très venteux": ":wind_blowing_face: :wind_blowing_face:", "Venteux et pluvieux": " :wind_blowing_face: :cloud_rain:", "Très venteux et pluvieux": ":wind_blowing_face: :wind_blowing_face: :cloud_rain:", "Tempête": ":cloud_tornado:", "Ouragan": ":cloud_tornado: :cloud_tornado:"}
    directions = ("Nord", "Nord-Est", "Est", "Sud-Est", "Sud", "Sud-Ouest", "Ouest", "Nord-Ouest")
    temperature = random.randint(-10, 25)
    vent = random.randint(0, 130)
    direction = random.choice(directions)
    if vent < 6:
        temps = "Calme"
    elif vent >= 6 and vent < 25:
        temps = random.choice(("Calme", "Pluvieux"))
    elif vent >= 25 and vent < 50:
        temps = random.choice(("Venteux", "Venteux et pluvieux"))
    elif vent >= 50 and vent < 80:
        temps = random.choice(("Très venteux", "Très venteux et pluvieux"))
    elif vent >= 80 and vent < 100:
        temps = "Tempête"
    else:
        temps = "Ouragan"
    embed_rep.clear_fields()
    embed_rep.set_footer(text="Météo du Nolarien")
    embed_rep.add_field(name=f"Météo {correspondance[temps]}", value=f"Voici les conditions météo du jour actuel: \n:white_small_square: {temperature}°C \n:white_small_square: {temps} \n:white_small_square: {vent}km/h en direction du {direction}")
    if temps == "Tempête":
        embed_rep.add_field(name="Alerte", value="Tempête :warning:")
    elif temps == "Ouragan":
        embed_rep.add_field(name="Alerte", value=":warning: **Ouragan** :warning: \n*Recommandations aux populations: ne sortez en aucun cas, restez abrité sous terre ou dans un abri adapté. Suivez les consignes nationales.*")
    await ctx.send(embed=embed_rep)

#Wide
@bot.command(name="wide", help="Mystère !")
@discord.ext.commands.has_permissions(administrator=True)
async def wide(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/537667794112610314/1084138741670625511/Wide2.mp4")

@wide.error
async def wide_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(embed=erreur_permissions())

#Embed_creator
@bot.command(name="embed_creator", help="Permet de créer facilement des messages embeds.")
@discord.ext.commands.has_permissions(administrator=True)
async def embed_creator(ctx):
    dico_info = {"title": None, "fields": None, "footer_text": None, "footer_icon": None, "image": None, "thumbnail": None, "color": discord.Colour.blue(), "channel": ctx}
    correspondance_anglais_francais = {"title": "Titre", "fields": "Champs de texte", "footer_text": "Note de pied de page", "footer_icon": "Icône de pied de page", "image": "Image", "thumbnail": "Miniature", "color": "Couleur", "channel": "Salon"}
    liste_actions = ["title", "fields", "footer_text", "footer_icon", "image", "thumbnail", "color", "channel"]
    messages = {"title": "Indiquez le titre de l'embed.", 
                "field_name": """Indiquez le titre du champ de texte. Si vous ne souhaitez pas ajouter d'autres champs, indiquez "N" """, 
                "field_value": "Indiquez le contenu du champ de texte.", 
                "footer_text": "Indiquez le contenu de la note de pied de page.", 
                "footer_icon": "Indiquez l'URL de l'icône de la note de pied de page.", 
                "image": "Indiquez l'URL d'une image à inclure en bas de l'embed.", 
                "thumbnail": "Indiquez l'URL d'une image servant de miniature (en haut à droite).",
                "color": """Indiquez le couleur de la bande de l'embed, soit sous un format héxadécimal avec un #, soit un triplet de valeurs RGB ("#009ce9" ou "12 156 233"). Reste bleue si None.""",
                "channel": """Indiquez, en le "mentionnant", le salon dans lequel le message doit être envoyé. None indiquera le salon actuel."""}
    #Pour des questions de simplicité, la création des embeds se fera de manière "interactive", avec des questions/réponses.
    
    embed_interface = discord.Embed(color = discord.Color.blue(), title="Création d'embed")
    embed_interface.add_field(name = "Initialisation", value=""":small_blue_diamond: Bienvenue sur la création de votre embed !
:white_small_square: Assurez-vous de répondre de façon claire et sans erreur, notamment pour les URL d'images.
:white_small_square: Lorsque qu'un champ doit rester vide, entrez "None". Si vous souhaitez arrêter, envoyez "STOP".""")
    embed_interface.set_footer(text = "Uchronia", icon_url = URL_LOGO)
    await ctx.send(embed=embed_interface)
    embed_interface.clear_fields()
    
    #Nombre d'étapes
    total = len(liste_actions)
    #Rang de l'étape
    rang = 1
    
    liste_fields = []
    
    for element in liste_actions:
        
        if element == "fields":
            embed_interface.add_field(name=f"{correspondance_anglais_francais[element]} ({rang}/{total})", value="""Vous allez pouvoir ajouter plusieurs champs de texte. Une fois terminé, indiquez "N". """)
            await ctx.send(embed=embed_interface)
            embed_interface.clear_fields()
            
            titre_champ = None
        
            while titre_champ != "N":
                embed_interface.add_field(name=f"{correspondance_anglais_francais[element]} ({rang}/{total})", value=messages["field_name"])
                await ctx.send(embed=embed_interface)
                embed_interface.clear_fields()
                
                msg = await bot.wait_for("message", check= lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)
                titre_champ = msg.content
                
                if titre_champ == "N":
                    break
                
                embed_interface.add_field(name=f"{correspondance_anglais_francais[element]} ({rang}/{total})", value=messages["field_value"])
                await ctx.send(embed=embed_interface)
                embed_interface.clear_fields()
                
                msg = await bot.wait_for("message", check= lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)
                valeur_champ = msg.content
                
                liste_fields.append((titre_champ, valeur_champ))
        else:
            embed_interface.add_field(name=f"{correspondance_anglais_francais[element]} ({rang}/{total})", value=messages[element])
            await ctx.send(embed=embed_interface)
            embed_interface.clear_fields()
        
            msg = await bot.wait_for("message", check= lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)
            reponse = msg.content
        
        rang += 1
        
        if element == "fields":
            reponse = liste_fields
        else:
            reponse = msg.content
        
        if reponse == "STOP":
            embed_tempo = embed_error.copy()
            embed_tempo.add_field(name = "Arrêt", value = "Vous avez mis fin à la création de votre embed.")
            await ctx.send(embed=embed_tempo)
            embed_tempo.clear_fields()
            return
        
        if reponse != "None":
            if element == "color":
                if reponse[0] != "#":
                    #On transforme le triplet en chaîne héxadécimale de caractères
                    reponse = '#%02x%02x%02x' % (int(reponse.split()[0]), int(reponse.split()[1]), int(reponse.split()[2]))
                reponse = discord.Colour.from_str(reponse)
            if element == "channel":
                #On récupère le salon via son ID. Si on avait laissé None, le salon utilisé serait celui où la commande est exécutée
                reponse = bot.get_channel(int(reponse[2:-1]))
            
            dico_info[element] = reponse
    
    #Création de l'embed
    embed_tempo = discord.Embed(colour = dico_info["color"], title = dico_info["title"])
    embed_tempo.set_image(url = dico_info["image"])
    embed_tempo.set_thumbnail(url = dico_info["thumbnail"])
    for couple in dico_info["fields"]:
        embed_tempo.add_field(name = couple[0], value = couple[1])
    embed_tempo.set_footer(text = dico_info["footer_text"], icon_url = dico_info["footer_icon"])
    
    channel = dico_info["channel"]
    await channel.send(embed=embed_tempo)
    
@embed_creator.error
async def embed_creator_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send(embed=erreur_permissions())



#################
### LANCEMENT ###
#################

bot.run(token)
