import asyncio
import discord
import random
import threading

from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands
from discord.ext.commands import errors
from cogs.UtilsLib import Utils

class Game(commands.Cog, Utils):
    """Commands that are related to the Emu Bot game. In this game, you can earn credits by chatting, buy emus with those credits, and attack other users with those credits, along with some other cool commands that help you get rich."""
    def __init__(self, bot):
        Utils.__init__(self)
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if (not message.author.id in self.SPAMCATCH) or (message.author.id in self.SPAMCATCH and not self.SPAMCATCH[message.author.id]):
            self.add_stats(message.author.id, 10, 'credits')
            self.SPAMCATCH[message.author.id] = True
            def spamtimer():
                self.spamswitch(message.author.id)
            t = threading.Timer(10.0, spamtimer)
            t.start()
    
    @commands.command(name = "stats",
                      description = "Displays your stats",
                      aliases = ["s"],
                      brief = "Displays your stats",
                      help = "Shows you the amount of credits you have, the number of emus in your storage, and the number of emus you have defense.",
                      usage = "[@user] (if no mention is provided, then it displays your stats)"
)
    async def stats(self, ctx, mention = None):
        if not mention == None:
            user = ctx.message.mentions[0]
            person = "{} has".format(user.name)
        else:
            user = ctx.author
            person = 'You have'
        idfu = user.id
        msg = "{0.mention}'s Stats:".format(user)
        msg += "\n:moneybag: {} `{}` credit(s).".format(person, self.get_stats(idfu, 'credits'))
        msg += "\n<:emu:439821394700926976> {} `{}` emu(s) in storage.".format(person, self.get_stats(idfu, 'storage'))
        msg += "\n:shield: {} `{}` emu(s) on defense.".format(person, self.get_stats(idfu, 'defense'))
        await ctx.send(msg)
    
    @commands.command(name = "defend",
                      description = "Puts emus on defense",
                      aliases = ['d', 'def', 'defense', 'defence'],
                      brief = "Puts emus on defense",
                      help = "Puts emus on defense. Emus on defense can protect against attacks.",
                      usage = "[# of emus]"
)
    async def defend(self, ctx, numemus: int):
        if not self.get_stats(ctx.author.id, 'storage') > 0:
            msg = 'You have no emus to put on defense! Remember, you can buy emus with e!buy!'
        elif numemus < 1:
            msg = "You can't put less than one emu on defense you trickster!"
        elif self.get_stats(ctx.author.id, 'defense') + numemus > self.MAXDEFENSE:
            msg = '{} more emu(s) on defense would be {} emu(s) over the maximum amount of emus allowed on defense. ({})'.format(numemus, (self.get_stats(ctx.author.id, 'defense') + numemus) - self.MAXDEFENSE, self.MAXDEFENSE)
        else:
            self.add_stats(ctx.author.id, numemus, 'defense')
            self.add_stats(ctx.author.id, -numemus, 'storage')
            msg = '`{}` emu(s) added to defense. You can check your stats with e!stats'.format(numemus)
        await ctx.send(msg)
        
    @commands.command(name = "offdefense",
                      description = "Takes emus off defense",
                      aliases = ['od', 'offdef' 'offdefence', 'offdefend'],
                      brief = "Takes emus off defense",
                      help = "Takes your emus off of defense and puts them back into your storage",
                      usage = "[# of emus]"
)
    async def offdefense(self, ctx, numemus: int):
        if not self.get_stats(ctx.author.id, 'defense') > 0:
            msg = 'You have no emus to take off defense! Remember, you can put emus on defense with e!defend!'
        elif numemus < 1:
            msg = "You can't take less than one emu off defense you trickster!"
        elif numemus > self.get_stats(ctx.author.id, 'defense'):
            msg = "You don't have that many emus on defense to take off!"
        else:
            self.add_stats(ctx.author.id, -numemus, 'defense')
            self.add_stats(ctx.author.id, numemus, 'storage')
            msg = '`{}` emu(s) taken off defense. You can check your stats with e!stats'.format(numemus)
        await ctx.send(msg)
        
    @commands.command(name = "give",
                      description = "Gives credits to another user",
                      aliases = ['gi'],
                      brief = "Gives credits to another user",
                      help = "Gifts other users your credits. Only do this if you really want to, because they will not give them back most likely.",
                      usage = "[number] [@mention]"
)
    async def give(self, ctx, numcreds: int, mention: str):
        uid = ctx.message.mentions[0].id
        if not self.get_stats(ctx.author.id, 'credits') > 0:
            msg = 'You have no credits to give!'
        elif numcreds < 1:
            msg = "You can't give less than one credit!"
        elif numcreds > self.get_stats(ctx.author.id, 'credits'):
            msg = "You don't have enough credits for that!"
        elif uid == self.bot.user.id:
            msg = "You can't give me credits!"
        elif uid == ctx.author.id:
            msg = "You can't give yourself credits!"
        else:
            self.add_stats(ctx.message.mentions[0].id, numcreds, 'credits')
            self.add_stats(ctx.author.id, -numcreds, 'credits')
            msg = 'You gave `{0}` credits to {1.message.mentions[0].mention}.'.format(numcreds, ctx)
        await ctx.send(msg)
        
    @commands.command(name = "attack",
                      description = "Attacks other users",
                      aliases = ['a', 'at', 'atk', 'attk'],
                      brief = "Attacks other users",
                      help = "Attacks other users with the emus you have in storage. If you attack with more emus than they have on defense, then you will steal some of their credits.",
                      usage = "[# of emus] [@user]"
)
    @commands.cooldown(1, Utils.ATTACKCOOLDOWN, BucketType.default)
    async def attack(self, ctx, numemus: int, mention: str):
        uid = ctx.message.mentions[0].id
        if numemus > self.get_stats(ctx.author.id, 'storage'):
            msg = "You don't have that many emus than you have in storage, you silly emu warlord! Remember, you can buy emus with e!buy!"
        elif numemus <= 0:
            msg = "You can't put less than one emu on attack!"
        elif numemus > self.MAXATTACK:
            msg = "That's more than you are allowed to send on attack. ({})".format(self.MAXATTACK)
        elif uid == self.bot.user.id:
            msg = "You can't attack me!!!"
        elif uid == ctx.author.id:
            msg = "You can't attack yourself!"
        else:
            prebattlecredits = self.get_stats(uid, 'credits')
            creditcalnum = self.CREDITSPEMUATK * (numemus - self.get_stats(uid, 'defense'))
            #checks if user broke other user's defenses
            if creditcalnum < 0:
                self.add_stats(uid, -numemus, 'defense')
                creditcalnum = 0
            else: #  if user broke other user's defenses
                #  checks if user being attacked can pay attackee
                if prebattlecredits - creditcalnum < 0:
                    self.add_stats(ctx.author.id, prebattlecredits, 'credits')
                    self.add_stats(uid, -prebattlecredits, 'credits')
                    creditcalnum = 0
                else: 
                    self.add_stats(ctx.author.id, creditcalnum, 'credits')
                    self.add_stats(uid, -creditcalnum, 'credits')
                self.add_stats(uid, -self.get_stats(uid, 'defense'), 'defense')
            self.add_stats(ctx.author.id, -numemus, 'storage')
            msg = '{} was attacked by {} with `{}` emu(s) and now has `{}` emu(s) left on defense, {} stole `{}` credits.'.format(ctx.message.mentions[0].mention, ctx.author.mention, str(numemus), self.get_stats(uid, 'defense'), ctx.author.mention, str(creditcalnum))
        if not ctx.author.id in self.ATTACKED:
            self.ATTACKED[ctx.author.id] = False
        await ctx.send(msg)
    
    @attack.after_invoke
    async def remove_cooldown(self, ctx):
        if 448272810561896448 in [role.id for role in ctx.author.roles] or not self.ATTACKED:
            self.attack.reset_cooldown(ctx)
        self.ATTACKED[ctx.author.id] = False

    @attack.error
    async def attack_error_handler(self, ctx, error):
        if not isinstance(error, errors.CommandOnCooldown):
            if isinstance(error, errors.BadArgument):
                msg = "You put the wrong type of value for one of the parameters for this command. Use `e!help attack` to find out how to use it correctly."
            elif isinstance(error, errors.MissingRequiredArgument):
                msg = "You did not give a required parameter for this command. Use `e!help attack` to find what you were missing."
            else:
                msg = error
                print('Message', ctx.message.content, 'caused exception:')
                print(error)
                print(type(error))
            self.attack.reset_cooldown(ctx)
        else:
            msg = error
        await ctx.send(msg)

    @commands.group(name = "buy",
                    description = "Buys emus",
                    aliases = ["b"],
                    brief = "Buys emus",
                    help = "Use this command to buy emus which go into your storage. Remember, you can only have a maximum of 20 emus.",
                    usage = "[# of emus]",
                    invoke_without_command = True,
                    case_insensitive = True
)
    async def buy(self, ctx, numemus: int):
        val = self.get_stats(ctx.author.id, 'credits')
        if numemus < 1 or numemus + self.get_stats(ctx.author.id, 'storage') + self.get_stats(ctx.author.id, 'defense') > self.MAXEMUS:
            if numemus < 1:
                msg = "You can't buy less than one emu you trickster!"
            if numemus + self.get_stats(ctx.author.id, 'storage') + self.get_stats(ctx.author.id, 'defense') > self.MAXEMUS:
                msg = "That is more than the maximum number of emus you can have! ({})".format(str(self.MAXEMUS))
        else:
            if self.get_stats(ctx.author.id, 'credits') < self.EMUPRICE * numemus:
                msg = "You have `{}` credits.\nThe number of emus you want to buy cost `".format(val) + str(self.EMUPRICE * numemus) + "` credits. You do not have enough credits to buy those emus."
            else:
                self.ASKEDFORBUYEMU = {ctx.author.id: {}}
                self.ASKEDFORBUYEMU[ctx.author.id]['started'] = True
                self.ASKEDFORBUYEMU[ctx.author.id]['numemus'] = numemus
                msg = "You have `{}` credits.\n{} emu(s) costs `{}` credits. If you would like to buy an emu, say e!buy yes. Say e!buy no to cancel.".format(val, numemus, self.EMUPRICE * numemus)
        await ctx.send(msg)
    
    @buy.command(name = "yes",
                 aliases = ["y"],
                 hidden = True
)
    async def buyconfirm(self, ctx):
        if not ctx.author.id in self.ASKEDFORBUYEMU or not self.ASKEDFORBUYEMU[ctx.author.id]['started']:
            msg = "You did not ask to buy an emu yet..."
        else:
            numemus = self.ASKEDFORBUYEMU[ctx.author.id]['numemus']
            self.ASKEDFORBUYEMU[ctx.author.id]['numemus'] = None
            self.ASKEDFORBUYEMU[ctx.author.id]['started'] = False
            self.add_stats(ctx.author.id, -(self.EMUPRICE * numemus), 'credits')
            self.add_stats(ctx.author.id, (numemus), 'storage')
            msg = '''You bought `''' + str(numemus) + '''` emu(s)! Use e!stats to see your stats'''
        await ctx.send(msg)
    
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
        await ctx.send(msg)
    
    @commands.group(name = "reset",
                    description = "Resets all of your stats",
                    aliases = ["r"],
                    brief = "Resets all of your stats",
                    help = "Resets all of your stats back to 0, restarting your experience with the emu bot game",
                    invoke_without_command = True,
                    case_insensitive = True
)
    async def reset(self, ctx):
        self.ASKEDFORRESET[ctx.author.id] = True
        msg = '''Are you sure you want to reset ***all*** of your stats? You'll lose everything! If you're sure, use e!reset yes. To cancel, say e!reset no'''
        await ctx.send(msg)
    
    @reset.command(name = 'yes',
                  aliases = ['y'],
                  hidden = True
)
    async def resetconfirm(self, ctx):
        caid = ctx.author.id
        if caid in self.ASKEDFORRESET and self.ASKEDFORRESET[caid]:
            self.ASKEDFORRESET[caid] = False
            cred = self.get_stats(caid, 'credits')
            store = self.get_stats(caid, 'storage')
            defse = self.get_stats(caid, 'defense')
            self.add_stats(caid, -cred, 'credits')
            self.add_stats(caid, -store, 'storage')
            self.add_stats(caid, -defse, 'defense')
            msg = 'All of your stats have been reset.'
        else:
            msg = 'You did not ask to reset your stats yet!'
        await ctx.send(msg)
        
    @reset.command(name = 'no',
                   aliases = ['n'],
                   hidden = True
)
    async def resetcancel(self, ctx):
        caid = ctx.author.id
        if caid in self.ASKEDFORRESET and self.ASKEDFORRESET[caid]:
            self.ASKEDFORRESET[caid] = False
            msg = 'Canceled'
        else:
            msg = 'You did not ask to reset your stats yet!'
        await ctx.send(msg)
        
    @commands.command(name = "getcredits",
                      aliases = ["gc"],
                      hidden = True)
    @commands.has_role('Tester')
    async def getcredits(self, ctx, numcredits: int):
        self.add_stats(ctx.author.id, numcredits, 'credits')
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
    
def setup(bot):
    bot.add_cog(Game(bot))
