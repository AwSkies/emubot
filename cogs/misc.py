import discord

from discord.ext import commands
from cogs.UtilsLib import Utils

class Misc(commands.Cog, Utils):
    """Commands that don't really fit into any other category."""
    def __init__(self, bot):
        Utils.__init__(self)
        self.bot = bot

    @commands.command(name = "say",
                      description = "Makes the bot say whatever you say",
                      brief = "Makes the bot say whatever you say",
                      help = "Makes the bot says whatever you put after the e!say",
                      usage = '[sentence or "sentence"] - makes the bot say [sentence or "sentence"]'
)
    async def say(self, ctx, *args):
        if len(args) == 0:
            msg = "You can't make me send an empty message!"
            await ctx.send(msg)
        else:
            embed = discord.Embed(color = ctx.author.roles[-1].color)
            name = 'The Emu says:'
            if len(args) == 1:
                embed.add_field(name = name, value = args[0], inline=False)
            else:
                embed.add_field(name = name, value = ' '.join(args), inline=False)
            embed.set_footer(text = "-" + str(ctx.author))
            await ctx.message.delete()
            await ctx.send(embed=embed)

    @commands.command(name = "helpersay",
                      aliases = ["hsay", "hs"],
                      hidden = True
)
    @commands.has_role('Helpers')
    async def helpersay(self, ctx, *args):
        if len(args) == 0:
            msg = "You can't make me send an empty message!"
        elif len(args) == 1:
            msg = args[0]
        else:
            msg = ' '.join(args)
        await ctx.message.delete()
        await ctx.send(msg)
        
    @commands.command(name = "changestatus",
                      aliases = ["cs"],
                      hidden = True
)
    @commands.is_owner()
    async def changegamestatus(self, ctx, *args):
        if len(args) == 0:
            gamename = "Say e!help"
        elif len(args) == 1:
            gamename = args[0]
        else:
            gamename = ' '.join(args)
        game = discord.Game(name = gamename)
        msg = "Status changed to " + gamename
        await self.bot.change_presence(activity = game)
        await ctx.send(msg)
    
def setup(bot):
    bot.add_cog(Misc(bot))
