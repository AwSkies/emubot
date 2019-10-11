import discord

from discord.ext import commands
from masterclass import masterclass

class Misc(masterclass):
    def __init__(self, bot):
        super().__init__()
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
            embed=discord.Embed(color = 0x9bb0c8)
            if len(args) == 1:
                embed.add_field(value = args[0], inline=False)
            else:
                embed.add_field(value = ' '.join(args), inline=False)
            embed.set_footer(text = "-" + str(ctx.author))
            await ctx.send(embed=embed)

    @commands.command(name = "gamexplain",
                      description = "Gives an explanation to how the Emu Bot game works",
                      aliases = ['gx', 'gameexplain', 'gxplain']
                      brief = "Gives an explanation to how the Emu Bot game works",
                      help = "Gives an in-depth explain of how to use the Emu Bot's game commands and how the Emu Bot game works"
                      usage = 'e!gamexplain'
)
    async def gamexplain(self, ctx):
        embed = discord.Embed(title='Game Explanation', description='''**In the emu bot game, you gain credits by participating in chat. You can spend these credits on emus and attack your friends with them.**
-You earn credits by sending messages.
-You can use those credits to buy emus
-The maximum amount of emus you can have is {} emus
-You can put emus on defense
-The maximum amount of emus on defense is {} emus
-You can also use emus to attack your friends
-The maximum amount of emus you can attack with at a time is {} emus
-The amount of emus you attack someone with that go over the amount of emus they have on defense grants you 700 credits for each emu.'''.format(self.MAXEMUS, self.MAXDEFENSE, self.MAXATTACK), color=0x00ff00)
        ctx.send(embed = embed)
        
    @commands.command(name = "testersay",
                      aliases = ["tsay", "ts"]
                      hidden = True
)
    @commands.has_role('Tester')
    async def testersay(self, ctx, *args):
        if len(args) == 0:
            msg = "You can't make me send an empty message!"
        elif len(args) == 1:
            msg = args[0]
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
        
    @commands.command(name = "fillmeup",
                      aliases = ["fill", "fillup", "fmu", "fm"],
                      hidden = True)
    @commands.has_role('Tester')
    async def testerfill(self, ctx):
        #sets stats to 0
        self.add_stats(ctx.author.id, -self.get_stats(ctx.author.id, 'credits'), 'credits')
        self.add_stats(ctx.author.id, -self.get_stats(ctx.author.id, 'storage'), 'storage')
        self.add_stats(ctx.author.id, -self.get_stats(ctx.author.id, 'defense'), 'defense')
        #adds 20000 credits and the max amount of emus
        self.add_stats(ctx.author.id, 20000, 'credits')
        self.add_stats(ctx.author.id, self.MAXEMUS - self.MAXDEFENSE, 'storage')
        self.add_stats(ctx.author.id, self.MAXDEFENSE, 'defense')
        msg = 'You are maxed out, tester!'
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
                msg = "Status changed to " + args[0]
                game = discord.Game(name = args[0])
            else:
                msg = "Status changed to " + ' '.join(args)
                game = discord.Game(name = ' '.join(args))
            await bot.change_presence(game)
        await ctx.send(msg)
    
def setup(bot):
    bot.add_cog(Misc(bot))
