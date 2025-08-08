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
    async def on_command_error(ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            await ctx.send("Commande inconnue.")
        elif isinstance(error, discord.ext.commands.MissingPermissions):
            await ctx.send("Vous ne disposez pas des permissions requises.")
        else:
            await ctx.send("Erreur inconnue. Contactez un administrateur.")


    @commands.command(name="reload_extension", help="Recharge l'extension indiquée.")
    async def reload_bot_extension(self, extension):
        await self.bot.reload_extension(extension)
  

    @commands.command(name="shutdown", help="Eteint le bot")
    @discord.ext.commands.has_permissions(administrator=True)
    async def shutdown(self):
        await self.bot.change_presence(status=discord.Status.offline, activity=None)
        embed = discord.Embed(colour = discord.Colour.red())
        embed.add_field(name=f"*Bip bip bip*",value=f"Uchro-Bot s'est correctement éteint.")
        await self.bot.get_channel(self.bot.log_channel_id).send(embed=embed)
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(BotManagement(bot))