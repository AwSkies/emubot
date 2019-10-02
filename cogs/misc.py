import discord

from discord.ext import commands
from masterclass import masterclass

class Misc(masterclass):
    def __init__(self, bot):
        super().__init()
        self.bot = bot

    @commands.command(name = "",
                      description = "",
                      aliases = [""],
                      brief = "",
                      help = "",
                      usage = ""
)
    async def (self, ctx, ):
    
def setup(bot):
    bot.add_cog(Misc(bot))
