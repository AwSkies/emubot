import discord

from discord.ext import commands
from masterclass import masterclass

class Game(masterclass):
    def __init__(self, bot):
        super().__init()
        self.bot = bot
    
    @commands.command(name = "stats",
                      description = "Displays your stats",
                      aliases = ["s"],
                      brief = "Displays your stats",
                      help = "Shows you the amount of credits you have, the number of emus in your storage, and the number of emus you have defense.",
                      usage = "e!stats [@mention] (if no mention is provided, then it displays your stats)"
)
    async def stats(self, ctx, mention = None):
        if not mention == None:
            #uidstr = the string version of the uid (Ex. <@!213676807651255>)
            uidstr = mention[1][2:-1]
            #checks if uid has a !
            if uidstr[0] == '!':
                uidstr = uidstr[1:]
            aid = uidstr
            msg = "<@" + uidstr + ">'s Stats:"
        else:
            mid = ctx.author.id
            msg = "{0.author.mention}'s Stats:".format(ctx)
        msg += "\n:moneybag: You have `{}` credits.".format(get_stats(aid, 'credits'))
        msg += "\n<:emu:439821394700926976> You have `{}` emu(s) in storage.".format(get_stats(aid, 'storage'))
        msg += "\n:shield: You have `{}` emu(s) on defense.".format(get_stats(aid, 'defense'))
        await ctx.send(msg)

    @commands.command(name = "",
                      description = "",
                      aliases = [""],
                      brief = "",
                      help = "",
                      usage = ""
)
    async def (self, ctx, ):
    
    @commands.command(name = "",
                      description = "",
                      aliases = [""],
                      brief = "",
                      help = "",
                      usage = ""
)
    async def (self, ctx, ):
    
def setup(bot):
    bot.add_cog(Game(bot))
