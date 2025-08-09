import discord
from discord.ext import commands
import random

class BotManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        # sends a message in shell
        print("""Uchro-Bot, a bot created for the french roleplay Discord server Uchronia.
© Waynd_d et Bastien Choulans, 2021-2025.
Coded in Python, with discord.py librairies.
              
The bot is ready ! Would you care to get a Great Depression for the road ?""")

        # sends a message in your log channel
        embed = discord.Embed(colour=discord.Colour.green())
        embed.add_field(name=f"Activation",value=f"Uchro-Bot a correctement été démarré.")
        await self.bot.get_channel(self.bot.log_channel_id).send(embed=embed)

        # sends a nice GIF in your log channel
        if random.randint(0, 50) == 25:
            await self.bot.get_channel(self.bot.log_channel_id).send("https://tenor.com/view/atomic-nuke-j-robert-oppenheimer-destroyer-of-the-worlds-death-gif-15159234")


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Commande inconnue.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Vous ne disposez pas des permissions requises.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Arguments manquants. Vérifiez la syntaxe de la commande.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("Une erreur est survenue lors de l'exécution de la commande.")
        else:
            await ctx.send(f"Erreur inconnue: {error}. Contactez un administrateur.")


    @commands.command(name="reload_extension", help="Recharge l'extension indiquée.")
    @commands.has_permissions(administrator=True)
    async def reload_bot_extension(self, ctx, extension: str):
        try:
            await self.bot.reload_extension(f"cogs.{extension}")
            await ctx.send(f"L'extension {extension} a été rechargée avec succès.")
        except Exception as e:
            await ctx.send(f"Erreur lors du rechargement de l'extension: {e}")


    @commands.command(name="shutdown", help="Éteint le bot")
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        try:
            log_channel = self.bot.get_channel(self.bot.log_channel_id)
            if log_channel:
                embed = discord.Embed(colour=discord.Colour.red())
                embed.add_field(name="*Bip bip bip*", value="Uchro-Bot s'est correctement éteint.")
                await log_channel.send(embed=embed)

            await ctx.send("Arrêt du bot en cours...")
            await self.bot.change_presence(status=discord.Status.offline, activity=None)
            await self.bot.close()
        except Exception as e:
            await ctx.send(f"Erreur lors de l'arrêt: {e}")
            
async def setup(bot):
    await bot.add_cog(BotManagement(bot))