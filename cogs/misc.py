import discord

from discord.ext import commands
from masterclass import masterclass

class Misc(masterclass):
    def __init__(self, bot):
        super().__init()
        self.bot = bot

    @commands.command(name = "say",
                      description = "Makes the bot say whatever you say",
                      aliases = ["s"],
                      brief = "Makes the bot say whatever you say",
                      help = "Makes the bot says whatever you put after the e!say",
                      usage = "e!say [sentence] or e!say, makes the bot say [sentence]"
)
    async def say(self, ctx, *args):
        if len(args) == 0:
            msg = "You can't make me send an empty message!"
        elif len(args) == 1:
            msg = ctx.author.mention + "says: \n" + args[1]
        else:
            msg = ctx.author.mention + "says: \n" + ' '.join(args)
        await ctx.send(msg)
        
    @commands.command(name = "msay",
                      aliases = ["sm"]
                      hidden = True
)
    async def say(self, ctx, *args):
        if len(args) == 0:
            msg = "You can't make me send an empty message!"
        elif len(args) == 1:
            msg = args[1]
        else:
            msg = ' '.join(args)
        await ctx.send(msg)
    
def setup(bot):
    bot.add_cog(Misc(bot))
