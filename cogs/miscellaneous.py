import discord
from discord.ext import commands

class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="ping", help="Renvoie la latence du bot")
    async def ping(self, ctx):
        await ctx.send(f":ping_pong: Latence: **{round(self.bot.latency * 1000)}** ms")


    @commands.command(name="wide", help="Mystère !")
    @discord.ext.commands.has_permissions(administrator=True)
    async def wide(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/537667794112610314/1084138741670625511/Wide2.mp4")


    @commands.command(name="brain_power", help="Mystère !")
    @discord.ext.commands.has_permissions(administrator=True)
    async def brain_power(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/1105818718518395020/1122980909453410364/Brain_Power.mp4")


    @commands.command(name="president", help="Mystère !")
    @discord.ext.commands.has_permissions(administrator=True)
    async def president(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/1105818718518395020/1123715876202483792/CHIRAC_-_Je_serai_le_president_de_tous_les_Francais_samba_remix_.mp4")
        

async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))