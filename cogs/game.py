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
            msg = "<@" + uidstr + ">'s Stats:"
            idfu = uidstr
        else:
            idfu = ctx.author.id
            msg = "{0.author.mention}'s Stats:".format(ctx)
        msg += "\n:moneybag: You have `{}` credits.".format(self.get_stats(idfu, 'credits'))
        msg += "\n<:emu:439821394700926976> You have `{}` emu(s) in storage.".format(self.get_stats(idfu, 'storage'))
        msg += "\n:shield: You have `{}` emu(s) on defense.".format(self.get_stats(idfu, 'defense'))
        await ctx.send(msg)

    @commands.group(name = "buy",
                    description = "Used to buy emus",
                    aliases = ["b"],
                    brief = "Used to buy emus",
                    help = "Use this command to buy emus which go into your storage. Remember, you can only have a maximum of 20 emus.",
                    usage = "e!buy"
                    invoke_without_command = True
)
    async def initbuy(self, ctx):
        val = self.get_stats(ctx.author.id, 'credits')
        if val < self.EMUPRICE:
            msg = "You have `{}` credits.\nAn emu costs `".format(val) + str(self.EMUPRICE) + "` credits. You do not have enough credits to buy even one emu."
        else:
            self.ASKEDFORBUYEMU[message.author.id] = True
            msg = '''You have `{}` credits.\nAn emu costs `'''.format(val) + str(self.EMURPICE) + '''` credits. If you would like to buy an emu, say yes, then the number of emus you would like to buy. (Ex. `yes 2`). Say no to cancel.'''
        await ctx.send(msg)
    
    @buy.command(name = "yes",
                 aliases = ["y"],
                 hidden = True
)
    async def buyconfirm(self, ctx, numemus: int):
        if not (ctx.author.id in self.ASKEDFORBUYEMU and self.ASKEDFORBUYEMU[ctx.author.id]):
            msg = "You did not ask to buy an emu yet..."
        else:
            if numemus < 1 or numemus + self.get_stats(message.author.id, 'storage') + self.get_stats(message.author.id, 'defense') > self.MAXEMUS:
                if numemus < 1:
                    msg = "You can't buy less than one emu you trickster!"
                if numemus + self.get_stats(message.author.id, 'storage') + self.get_stats(message.author.id, 'defense') > self.MAXEMUS:
                    msg = "That is more than the maximum number of emus you can have! ({})".format(str(self.MAXEMUS))
            else:
                val = self.get_stats(message.author.id, 'credits')
                if get_value(message.author.id, 'credits') < emuprice * numemus:
                    msg = "You have `{}` credits.\nThe number of emus you want to buy cost `".format(val) + str(emuprice * numemus) + "` credits. You do not have enough credits to buy those emus."
                else:
                    askedforbuyemu[message.author.id] = False
                    self.add_stats(message.author.id, -(emuprice * numemus), 'credits')
                    self.add_stats(message.author.id, (numemus), 'torage')
                    msg = '''You bought `''' + str(numemus) + '''` emu(s)! Use e!stats to see your stats'''
                    await client.send_message(message.channel, msg)
            self.ASKEDFORBUYEMU[message.author.id] = False       
        ctx.send(msg)
            
            
    @buy.command(name = "no",
                 aliases = ["n"],
                 hidden = True
)
    async def buycancel(self, ctx):
        if ctx.author.id in self.ASKEDFORBUYEMU and self.ASKEDFORBUYEMU[ctx.author.id]:
            self.ASKEDFORBUYEMU[ctx.author.id] = False
            msg = "Canceled"
        else:
            msg = "You didn't ask to buy an emu yet..."
        await bot.send(msg)
    
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
