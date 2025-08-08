import yaml
import discord

### LOAD CONFIGURATION

def load_config():
    try:
        with open('config.yml', 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        print("Erreur : Le fichier de configuration config.yml n'a pas été trouvé.")
        return None
    except yaml.YAMLError as e:
        print(f"Erreur lors de la lecture du fichier de configuration : {e}")
        return None