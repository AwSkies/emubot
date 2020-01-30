import discord
import json

from discord.ext import commands
from cogs.UtilsLib import Utils

class Rewards(commands.Cog, Utils):
    """Ways to set and view custom rewards that can be bought with credits earned in the Emu Bot game"""
    def __init__(self, bot):
        Utils.__init__(self)
        self.bot = bot
        
def setup(bot):
    bot.add_cog(Rewards(bot))
