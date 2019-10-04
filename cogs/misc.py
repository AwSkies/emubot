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
            await ctx.send(msg)
        else:
            embed=discord.Embed()
            if len(args) == 1:
                embed.add_field(value = args[1], inline=False)
            else:
                embed.add_field(value = ' '.join(args), inline=False)
            embed.set_footer(text = "-" + str(ctx.author))
            await ctx.send(embed=embed)
        
    @commands.command(name = "testersay",
                      aliases = ["tsay", "ts"]
                      hidden = True
)
    @commands.has_role('Tester')
    async def testersay(self, ctx, *args):
        if len(args) == 0:
            msg = "You can't make me send an empty message!"
        elif len(args) == 1:
            msg = args[1]
        else:
            msg = ' '.join(args)
        await ctx.send(msg)
        
    @commands.command(name = "getcredits",
                      aliases = ["gc"],
                      hidden = True)
    @commands.has_role('Tester')
    async def getcredits(self, ctx, numcredits: int):
        add_stats(ctx.author.id, numcredits, 'credits')
        msg = "Got `" + str(numcredits) + "` credits, tester!"
        await ctx.send(msg)
        
    
    @commands.command(name = "changestatus",
                      aliases = ["cs"],
                      hidden = True
)
    @commands.is_owner()
    async def changegamestatus(self, ctx, *args):
        if len(args) == 0:
            msg = "You can't change the status to nothing!"
        else:
            if len(args) == 1:
                msg = "Status changed to " + args[1]
                game = discord.Game(name = args[1])
            else:
                msg = "States change to " + ' '.join(args)
                game = discord.Game(name = ' '.join(args))
            await bot.change_presence(game)
        await ctx.send(msg)
    
def setup(bot):
    bot.add_cog(Misc(bot))
