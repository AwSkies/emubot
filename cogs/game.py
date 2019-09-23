import discord

from discord.ext import commands
from masterclass import masterclass

class Game(masterclass):
    def __init__(self, bot):
        super().__init()
        self.bot = bot
    
def setup(bot):
    bot.add_cog(Game(bot))
