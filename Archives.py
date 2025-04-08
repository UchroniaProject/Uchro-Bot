"""Quelques scripts archivés."""

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
    embed_tempo = discord.Embed(colour = discord.Colour.blue(), title = "Météo")
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
    embed_tempo.set_footer(text="Météo du Nolarien")
    embed_tempo.add_field(name=f"{correspondance[temps]}", value=f"Voici les conditions météo du jour actuel: \n:white_small_square: {temperature}°C \n:white_small_square: {temps} \n:white_small_square: {vent}km/h en direction du {direction}")
    if temps == "Tempête":
        embed_tempo.add_field(name="Alerte", value="Tempête :warning:")
    elif temps == "Ouragan":
        embed_tempo.add_field(name="Alerte", value=":warning: **Ouragan** :warning: \n*Recommandations aux populations: ne sortez en aucun cas, restez abrité sous terre ou dans un abri adapté. Suivez les consignes nationales.*")
    await ctx.send(embed=embed_tempo)
   
   
    
#Wide_bis
@bot.command(name="wide_bis", help="Mystère !")
@discord.ext.commands.has_permissions(administrator=True)
async def wide_bis(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/1105818718518395020/1106621209153654806/Wide_Putin_Walking_but_hes_always_in_frame_full_version._Reupload.mp4")

@wide_bis.error
async def wide_bis_error(ctx, error):
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
                reponse = await discord.ext.commands.TextChannelConverter().convert(ctx=ctx, argument=reponse[2:-1])

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



### STATISTIQUES_ROLL
@bot.command(name="statistiques_roll", help="Retourne des statistiques sur un lancer de dé")
async def statistiques_roll(ctx, tirage):
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
        for i in range(len(resultats_tirage)):
            nouveau_resultat = resultats_tirage.pop(0) + ajout
            resultats_tirage.append(nouveau_resultat)
        statistiques = {i:j for i in resultats_tirage for j in [resultats_tirage.count(i)]}

        mean = numpy.average(resultats_tirage)
        median = numpy.median(resultats_tirage)
        std = numpy.std(resultats_tirage)
        variance = numpy.var(resultats_tirage)
        reponse = f"Tirage étudié: {tirage}\nMoyenne: {round(mean, 2)}\nMédiane: {median}\nEcart-type: {round(std, 2)}\nVariance: {round(variance, 2)}"

    except:
        raise Exception

    embed_tempo = discord.Embed(colour = discord.Colour.blue(), title = "Statistique de jet de dé 🎲")
    embed_tempo.add_field(name=f"Résultat",value=reponse)
    await ctx.send(embed=embed_tempo)

@statistiques_roll.error
async def statistiques_roll_error(ctx):
    embed_error.clear_fields()
    embed_error.set_footer(text=f"Erreur")
    embed_error.add_field(name=f"Désolé !",value=f"Votre demande de statistiques n'a pas été reconnue. Contactez un maître de jeu si vous pensez rencontrer une erreur.")
    await ctx.send(embed = embed_error)