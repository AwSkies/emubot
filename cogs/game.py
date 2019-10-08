import discord

from discord.ext import commands
from masterclass import masterclass

class Game(masterclass):
    def __init__(self, bot):
        super().__init__()
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
    
    @commands.command(name = "defend",
                      description = "Puts emus on defense",
                      aliases = ['d', 'defense', 'defence'],
                      brief = "Puts emus on defense",
                      help = "Puts emus on defense. Emus on defense can protect against attacks.",
                      usage = "e!defend [number]"
)
    async def defend(self, ctx, numemus: int):
        if not get_stats(ctx.author.id, 'storage') > 0:
            msg = 'You have no emus to put on defense! Remember, you can buy emus with e!buy!'
        elif numemus < 1:
            msg = "You can't put less than one emu on defense you trickster!"
        elif get_stats(ctx.author.id, 'defense') + numemus > self.MAXDEFENSE:
            msg = '{} emus on defense would be {} emus over the maximum amount of emus allowed on defense. ({})'.format(numemus, (self.get_stats(ctx.author.id) + numemus) - self.MAXDEFENSE, self.MAXDEFENSE)
        else:
            self.add_stats(ctx.author.id, numemus, 'defense')
            self.add_stats(ctx.author.id, -numemus, 'storage')
            msg = '`{}` emu(s) added to defense. You can check you stats with e!stats'.format(numemus)
        await ctx.send(msg)
        
    @commands.command(name = "offdefense",
                      description = "Takes emus off defense",
                      aliases = ['od', 'offdefence', 'offdefend'],
                      brief = "Takes emus off defense",
                      help = "Takes your emus off of defense and puts them back into your storage",
                      usage = "e!offdefense [number]"
)
    async def offdefense(self, ctx, numemus: int):
        if not get_stats(ctx.author.id, 'defense') > 0:
            msg = 'You have no emus to take off defense! Remember, you can put emus on defense with e!defend!'
        elif numemus < 1:
            msg = "You can't take less than one emu off defense you trickster!"
        elif numemus > get_stats(ctx.author.id, 'defense'):
            msg = "You don't have that many emus on defense to take off!"
        else:
            self.add_stats(ctx.author.id, numemus, 'defense')
            self.add_stats(ctx.author.id, -numemus, 'storage')
            msg = '`{}` emu(s) added to defense. You can check you stats with e!stats'.format(numemus)
        await ctx.send(msg)
        
    @commands.command(name = "",
                      description = "",
                      aliases = [""],
                      brief = "",
                      help = "",
                      usage = ""
)
    async def (self, ctx, ):

    @commands.group(name = "buy",
                    description = "Buys emus",
                    aliases = ["b"],
                    brief = "Buys emus",
                    help = "Use this command to buy emus which go into your storage. Remember, you can only have a maximum of 20 emus.",
                    usage = "e!buy"
                    invoke_without_command = True
                    case_insensitive = True
)
    async def buy(self, ctx):
        val = self.get_stats(ctx.author.id, 'credits')
        if val < self.EMUPRICE:
            msg = "You have `{}` credits.\nAn emu costs `".format(val) + str(self.EMUPRICE) + "` credits. You do not have enough credits to buy even one emu."
        else:
            self.ASKEDFORBUYEMU[message.author.id] = True
            msg = '''You have `{}` credits.\nAn emu costs `'''.format(val) + str(self.EMURPICE) + '''` credits. If you would like to buy an emu, say e!buy yes, then the number of emus you would like to buy. (Ex. `e!buy yes 2`). Say e!buy no to cancel.'''
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
    
    @commands.group(name = "reset",
                    description = "Resets all of your stats",
                    aliases = ["r"],
                    brief = "Resets all of your stats",
                    help = "Resets all of your stats back to 0, restarting your experience with the emu bot game",
                    usage = "e!reset"
                    invoke_without_command = True
                    case_insensitive = True
)
    async def reset(self, ctx):
        self.ASKEDFORRESET[ctx.author.id] = True
        msg = '''Are you sure you want to reset ***all*** of your stats? You'll lose everything! If you're sure, use e!reset yes. To cancel, say e!reset no'''
        await ctx.send(msg)
    
    @reset.command(name = 'yes'
                  aliases = ['y']
                  hidden = True
)
    async def resetconfirm(self, ctx):
        ctx.author.id = caid
        if caid in self.ASKEDFORRESET and self.ASKEDFORRESET[caid]
            self.ASKEDFORRESET[caid] = False
            cred = self.get_stats(caid, 'credits')
            store = self.get_stats(caid, 'storage')
            defse = self.get_stats(caid, 'defense')
            self.add_stats(caid, -stat, 'credits')
            self.add_stats(caid, -store, 'storage')
            self.add_stats(caid, -defse, 'defense')
            msg = 'All of your stats have been reset.'
        else:
            msg = 'You did not ask to reset your stats yet!'
        await ctx.send(msg)
        
    @reset.command(name = 'no'
                   aliases = ['n']
                   hidden = True
)
    async def resetcancel(self, ctx):
        ctx.author.id = caid
        if caid in self.ASKEDFORRESET and self.ASKEDFORRESET[caid]
            self.ASKEDFORRESET[caid] = False
            msg = 'Canceled'
        else:
            msg = 'You did not ask to reset your stats yet!'
        await ctx.send(msg)
    
def setup(bot):
    bot.add_cog(Game(bot))
