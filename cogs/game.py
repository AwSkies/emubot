import asyncio
import discord
import json
import math
import random
import threading
import time

from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands, tasks
from discord.ext.commands import errors
from cogs.UtilsLib import Utils

class Game(commands.Cog, Utils):
    """Commands that are related to the Emu Bot game. In this game, you can earn credits by chatting, buy emus with those credits, and attack other users with those credits, along with some other cool commands that help you get rich."""
    def __init__(self, bot):
        Utils.__init__(self)
        self.bot = bot
        self.loan_check.start()
        self.loans = {}
        #tracemalloc.start()
        
    def cog_unload(self):
        self.loan_check.cancel()
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if ((not message.author.id in self.SPAMCATCH) or (message.author.id in self.SPAMCATCH and not self.SPAMCATCH[message.author.id])) and (not self.is_disabled(message.author.id)):
            self.add_stats(message.author.id, 10, 'credits')
            self.SPAMCATCH[message.author.id] = True
            def spamtimer():
                self.spamswitch(message.author.id)
            t = threading.Timer(10.0, spamtimer)
            t.start()
    
    @commands.group(
        name = "stats",
        description = "Displays your stats",
        aliases = ["s"],
        brief = "Displays your stats",
        help = "Shows you the amount of credits you have, the number of emus in your storage, and the number of emus you have defense.",
        usage = "[@user] (if no mention is provided, then it displays your stats)",
        invoke_without_command = True,
        case_insensitive = True
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
        
    @stats.group(
        name = "disable",
        description = "Disable your participation in the Emu Bot game",
        aliases = ['d'],
        brief = "Stop being able to use stats",
        help = "If you disable your stats you will be unable to earn credits by chatting and will be unable to use stats or buy emus. You will not be able to attack other users but you will not be able to be attacked. You will also lose all of your current stats",
        invoke_without_command = True,
        case_insensitive = True
)
    async def disable_stats(self, ctx):
        if self.is_disabled(ctx.author.id):
            msg = 'Your stats are already disabled!'
        else:
            self.ASKEDFORDISABLESTATS[ctx.author.id] = True
            msg = 'Are you sure you want to disable your stats? This will make you unable to participate in the Emu Bot game or use any commands from the "Game" category, and reset all of your current stats. To confirm, use `e!stats disable yes`.'
        await ctx.send(msg)
        
    @disable_stats.command(
        name = 'yes',
        aliases = ['y'],
        hidden = True
)
    async def disable_confirm(self, ctx):
        caid = ctx.author.id
        if caid in self.ASKEDFORDISABLESTATS and self.ASKEDFORDISABLESTATS[caid]:
            self.ASKEDFORDISABLESTATS[caid] = False
            self.add_disabled(caid)
            msg = 'Your stats are now disabled.'
        else:
            msg = 'You did not ask to disable your stats yet!'
        await ctx.send(msg)
        
    @disable_stats.command(
        name = 'no',
        aliases = ['n'],
        hidden = True
)
    async def disable_cancel(self, ctx):
        caid = ctx.author.id
        if caid in self.ASKEDFORDISABLESTATS and self.ASKEDFORDISABLESTATS[caid]:
            self.ASKEDFORDISABLESTATS[caid] = False
            msg = 'Canceled'
        else:
            msg = 'You did not ask to disable your stats yet!'
        await ctx.send(msg)
        
    @stats.command(
        name = "enable",
        description = "Reenable your participation in the Emu Bot game",
        aliases = ['e'],
        brief = "Use stats again",
        help = "Used to guess a number out of the range you specified using the gamble command. You must have previously specified the number of credits and the range."
)
    async def enable_stats(self, ctx):
        caid = ctx.author.id
        if not self.is_disabled(caid):
            msg = 'Your stats are already enabled!'
        else:
            self.remove_disabed(caid)
            self.add_stats(ctx.author.id, -self.get_stats(ctx.author.id, 'credits'), 'credits')
            self.add_stats(ctx.author.id, -self.get_stats(ctx.author.id, 'storage'), 'storage')
            self.add_stats(ctx.author.id, -self.get_stats(ctx.author.id, 'defense'), 'defense')
            msg = 'Your stats are reenabled. You will now be able to earn credits by chatting, buy emus, and attack and be attacked.'
        await ctx.send(msg)
        
    async def cog_check(self, ctx):
        if (self.is_disabled(ctx.author.id) and (not ctx.command == self.enable_stats)) or ((not len(ctx.message.mentions) == 0) and self.is_disabled(ctx.message.mentions[0].id)):
            if ((self.is_disabled(ctx.author.id)) and (not ctx.command == self.enable_stats)):
                msg = 'You have disabled your stats and your participation in the Emu Bot game. To turn on your stats and be able to use all the commands in the "Game" category, use `e!stats enable`'
            elif ((not len(ctx.message.mentions) == 0) and self.is_disabled(ctx.message.mentions[0].id)):
                msg = 'That user has disabled their stats.'
            await ctx.send(msg)
            return False
        else: 
            return True
    
    @commands.command(
        name = "defend",
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
        
    @commands.command(
        name = "offdefense",
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
        
    @commands.command(
        name = "give",
        description = "Gives credits to another user",
        aliases = ['gi', 'gift'],
        brief = "Gives credits to another user",
        help = "Gifts other users your credits. Only do this if you really want to, because they will not give them back most likely.",
        usage = "[number] [@mention]"
)
    async def give(self, ctx, numcreds: int, mention: str):
        uid = ctx.message.mentions[0].id
        with open('loans.json', 'r') as f:
                loans = json.load(f)
        if str(ctx.author.id) in loans and loans[str(ctx.author.id)]['active']:
            msg = 'You cannot give credits while you have a loan taken out. Use `e!loan check` to check the status of your loan or `e!loan return` to return your loan.'
        elif not self.get_stats(ctx.author.id, 'credits') > 0:
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
        
    @commands.command(
        name = "attack",
        description = "Attacks other users",
        aliases = ['a', 'at', 'atk', 'attk'],
        brief = "Attacks other users",
        help = "Attacks other users with the emus you have in storage. If you attack with more emus than they have on defense, then you will steal some of their credits.",
        usage = "[# of emus] [@user]",
        cooldown_after_parsing = True
)
    @commands.cooldown(1, Utils.ATTACKCOOLDOWN, BucketType.user)
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
                    creditcalnum = prebattlecredits
                else: 
                    self.add_stats(ctx.author.id, creditcalnum, 'credits')
                    self.add_stats(uid, -creditcalnum, 'credits')
                self.add_stats(uid, -self.get_stats(uid, 'defense'), 'defense')
            self.add_stats(ctx.author.id, -numemus, 'storage')
            msg = '{} was attacked by {} with `{}` emu(s) and now has `{}` emu(s) left on defense, {} stole `{}` credits.'.format(ctx.message.mentions[0].mention, ctx.author.mention, str(numemus), self.get_stats(uid, 'defense'), ctx.author.mention, str(creditcalnum))
            self.ATTACKED[ctx.author.id] = True
        if not ctx.author.id in self.ATTACKED:
            self.ATTACKED[ctx.author.id] = False
        await ctx.send(msg)
    
    @attack.after_invoke
    async def remove_cooldown(self, ctx):
        if 448272810561896448 in [role.id for role in ctx.author.roles] or not self.ATTACKED[ctx.author.id]:
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
                print('-----')
        else:
            msg = error
        await ctx.send(msg)

    @commands.group(
        name = "buy",
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
                self.ASKEDFORBUYEMU[ctx.author.id] = {}
                self.ASKEDFORBUYEMU[ctx.author.id]['started'] = True
                self.ASKEDFORBUYEMU[ctx.author.id]['numemus'] = numemus
                msg = "You have `{}` credits.\n{} emu(s) costs `{}` credits. If you would like to buy an emu, say e!buy yes. Say e!buy no to cancel.".format(val, numemus, self.EMUPRICE * numemus)
        await ctx.send(msg)
    
    @buy.command(
        name = "yes",
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
    
    @buy.command(
        name = "no",
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
    
    @commands.group(
        name = "sell",
        description = "Sells emus",
        aliases = ["se", "sl"],
        brief = "Sells emus",
        help = "Use this command to sell emus from your storage for credits.",
        usage = "[# of emus]",
        invoke_without_command = True,
        case_insensitive = True
)
    async def sell(self, ctx, numemus: int):
        if numemus < 1 or numemus > self.get_stats(ctx.author.id, 'storage'):
            if numemus < 1:
                msg = "You can't buy sell than one emu you trickster!"
            if numemus > self.get_stats(ctx.author.id, 'storage'):
                msg = "That is more than the number of emus you have in your storage! ({})".format(str(self.get_stats(ctx.author.id, 'storage')))
        else:
            self.ASKEDFORSELLEMU[ctx.author.id] = {}
            self.ASKEDFORSELLEMU[ctx.author.id]['started'] = True
            self.ASKEDFORSELLEMU[ctx.author.id]['numemus'] = numemus
            msg = "You have `{}` emus.\n{} emu(s) sell for `{}` credits. If you would like to sell an emu, say e!sell yes. Say e!sell no to cancel.".format(self.get_stats(ctx.author.id, 'storage'), numemus, self.EMUSELLPRICE * numemus)
        await ctx.send(msg)
    
    @sell.command(
        name = "yes",
        aliases = ["y"],
        hidden = True
)
    async def sellconfirm(self, ctx):
        if not ctx.author.id in self.ASKEDFORSELLEMU or not self.ASKEDFORSELLEMU[ctx.author.id]['started']:
            msg = "You did not ask to sell an emu yet..."
        else:
            numemus = self.ASKEDFORSELLEMU[ctx.author.id]['numemus']
            self.ASKEDFORSELLEMU[ctx.author.id]['numemus'] = None
            self.ASKEDFORSELLEMU[ctx.author.id]['started'] = False
            self.add_stats(ctx.author.id, (self.EMUSELLPRICE * numemus), 'credits')
            self.add_stats(ctx.author.id, -(numemus), 'storage')
            msg = '''You sold `''' + str(numemus) + '''` emu(s)! Use e!stats to check your stats.'''
        await ctx.send(msg)
    
    @sell.command(
        name = "no",
        aliases = ["n"],
        hidden = True
)
    async def sellcancel(self, ctx):
        if ctx.author.id in self.ASKEDFORSELLEMU and self.ASKEDFORSELLEMU[ctx.author.id]:
            self.ASKEDFORSELLEMU[ctx.author.id] = False
            msg = "Canceled"
        else:
            msg = "You didn't ask to sell an emu yet..."
        await ctx.send(msg)
    
    @commands.group(
        name = "reset",
        description = "Resets all of your stats",
        aliases = ["re", 'res'],
        brief = "Resets all of your stats",
        help = "Resets all of your stats back to 0, restarting your experience with the emu bot game",
        invoke_without_command = True,
        case_insensitive = True
)
    async def reset(self, ctx):
        self.ASKEDFORRESET[ctx.author.id] = True
        msg = '''Are you sure you want to reset ***all*** of your stats? You'll lose everything! If you're sure, use e!reset yes. To cancel, say e!reset no'''
        await ctx.send(msg)
    
    @reset.command(
        name = 'yes',
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
            with open('loans.json', 'r') as f:
                loans = json.load(f)
            if str(ctx.author.id) in loans and loans[str(ctx.author.id)]['active']:
                del loans[str(ctx.author.id)]
                with open('loans.json', 'w') as f:
                    json.dump(loans, f, sort_keys = False, indent = 4)
            msg = 'All of your stats have been reset.'
        else:
            msg = 'You did not ask to reset your stats yet!'
        await ctx.send(msg)
        
    @reset.command(
        name = 'no',
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
        
    @commands.group(
        name = "gamble",
        description = "Let's roll the dice...",
        aliases = ["g"],
        brief = "Gambles your credits (or your life) away...",
        help = "Pick a number between 1 and a number of your choice, and if you win you will get an amount of credits equal to the credits you gambled time a number proportional to the amount of numbers you picked from.",
        usage = "[number of credits to gamble] [number of # to choose from]",
        invoke_without_command = True,
        case_insensitive = True
)
    async def gamble(self, ctx, numcreds: int, gamblerange: int):
        if numcreds > self.get_stats(ctx.author.id, 'credits'):
            msg = "You don't have that number of credits to gamble!"
        elif numcreds < 1:
            msg = "You can't gamble less than one credit!"
        elif gamblerange <= 1:
            msg = "You can't pick from one or less than one number!"
        else:
            msg = 'Use `e!gamble guess [number]` to pick a number between **1** and **{}**. If you wish to cancel, `e!gamble cancel` "cancel".'.format(gamblerange)
            self.GAMBLEINFO[ctx.author.id] = {}
            self.GAMBLEINFO[ctx.author.id]['started'] = True
            self.GAMBLEINFO[ctx.author.id]['range']   = gamblerange
            self.GAMBLEINFO[ctx.author.id]['credits'] = numcreds
        await ctx.send(msg)
    
    @gamble.command(
        name = "guess",
        description = "Used to guess a number out of the range you specified using the gamble command",
        aliases = ['g'],
        brief = "Used to guess a number",
        help = "Used to guess a number out of the range you specified using the gamble command. You must have previously specified the number of credits and the range.",
        usage = '[number]'
)
    async def gambleguess(self, ctx, guessnum: int):
        if (not ctx.author.id in self.GAMBLEINFO) or (not self.GAMBLEINFO[ctx.author.id]['started']):
            msg = "You haven't made a gamble yet! Use e!gamble if you wish to."
            await ctx.send(msg)
        else:
            gamblerange = self.GAMBLEINFO[ctx.author.id]['range']
            numcreds = self.GAMBLEINFO[ctx.author.id]['credits']
            if guessnum < 1 or guessnum > gamblerange:
                msg = 'Pick a number between **1** and **{}**. If you wish to cancel, use e!gamble cancel.'.format(gamblerange)
                await ctx.send(msg)
            else:
                num = random.randint(1, gamblerange)
                def dicepicker():
                    dicefaces = ['<:dice1:559092222545625089>', '<:dice2:559092223044485140>', '<:dice3:559092223040552970>', '<:dice4:559092222935564301>', '<:dice5:559092223052873739>', '<:dice6:559092223145279491>']
                    face1 = random.choice(dicefaces)
                    face2 = random.choice(dicefaces)
                    msg = 'Rolling the dice...' + face1 + face2
                    return msg
                msg = await ctx.send(dicepicker())
                await asyncio.sleep(0.85)
                for _ in range(2):
                    await msg.edit(content = dicepicker())
                    await asyncio.sleep(0.85)
                if not num == guessnum:
                    self.add_stats(ctx.author.id, -numcreds, "credits")
                    await msg.edit(content = 'Sorry, the number was `{}`. You lost `{}` credits... :('.format(num, numcreds))
                else:
                    credcalnum = numcreds * int(gamblerange / 2)
                    self.add_stats(ctx.author.id, credcalnum, 'credits')
                    self.GAMBLEINFO[ctx.author.id]['started'] = False
                    self.GAMBLEINFO[ctx.author.id]['range']   = None
                    self.GAMBLEINFO[ctx.author.id]['credits'] = None
                    await msg.edit(content = ':confetti_ball: You won!!! You gained `{}` credits! :tada:'.format(credcalnum))
        
    @gamble.command(
        name = "cancel",
        aliases = ['c', 'no', 'n'],
        hidden = True
)
    async def gamblecancel(self, ctx):
        if not self.GAMBLEINFO[ctx.author.id]['started'] or not ctx.author.id in self.GAMBLEINFO:
            msg = "You haven't made a gamble yet! Use e!gamble if you wish to."
        else:
            msg = 'Canceled'
            self.GAMBLEINFO[ctx.author.id]['started'] = False
        await ctx.send(msg)
    
    def calculate_loan(self, Principal: int, start: int):
        elapsed = int(time.time()) - start
        current = int(Principal * (Utils.LOANINTRATE / 60) * elapsed)
        if current < Principal:
            return Principal
        else:
            return current
    
    @commands.group(
        name = "loan",
        description = "Loans you credits with interest",
        aliases = ["l"],
        brief = "Loans you credits with interest",
        help = "Loans you however many credits you want for {}% interest per minute.".format(int((Utils.LOANINTRATE - 1.0) * 100)),
        usage = "[principal]",
        invoke_without_command = True,
        case_insensitive = True
)
    async def loan(self, ctx, principal: int):
        with open('loans.json', 'r') as f:
            loans = json.load(f)
        if principal < 1:
            msg = "You can't choose a principal less than one, silly!"
        elif principal > self.LOAN_CAP:
            msg = "You can't take out loans greater than `{}` credits!".format(self.LOAN_CAP)
        elif (str(ctx.author.id) in loans) and loans[str(ctx.author.id)]['active']:
            msg = "You already have a loan, and you can't get two at once! If you want to pay it off, say e!loan return."
        else:
            loans[str(ctx.author.id)] = {}
            loans[str(ctx.author.id)]['active'] = True
            loans[str(ctx.author.id)]['principal'] = principal
            loans[str(ctx.author.id)]['user_id'] = ctx.author.id
            startt = int(time.time())
            loans[str(ctx.author.id)]['start'] = startt
            t = int((principal / self.LOAN_CREDS_PER_HOUR) * 3600)   #calculate time for one hour, then convert to seconds
            loans[str(ctx.author.id)]['time'] = t + startt           #add calculated time to current time to get time at which loan is due
            with open('loans.json', 'w') as f:
                json.dump(loans, f, sort_keys = False, indent = 4)
            self.add_stats(ctx.author.id, principal, 'credits')
            h = int(math.floor(t / 3600))
            m = int(math.floor((t - (h * 3600)) / 60))
            s = int(math.floor(t - ((h * 3600) + (m * 60))))
            msg = "You were loaned `{}` credits with a {}% interest rate per minute! You must return your loan in `{}` hours `{}` minutes and `{}` seconds. Remember that final amount is calculated using simple interest and if you don't return your loan in time, all of your stats will be reset. You can return your loan at any time with e!returnloan, as long as you have enough money to.".format(principal, int((Utils.LOANINTRATE - 1.0) * 100), h, m, s)
        await ctx.send(msg)
        
    @loan.command(
        name = "check",
        description = "Displays info about your loan",
        aliases = ["c"],
        brief = "Displays info about your loan",
        help = "Checks how much time you have on your loan and how much money its for."
)
    async def checkloan(self, ctx):
        with open('loans.json', 'r') as f:
            loans = json.load(f)
        if (not str(ctx.author.id) in loans) or (not loans[str(ctx.author.id)]['active']):
            msg = "You don't have a loan to check..."
        else:
            now = int(time.time())
            t = int(loans[str(ctx.author.id)]['time'] - now)
            h = int(math.floor(t / 3600))
            m = int(math.floor((t - (h * 3600)) / 60))
            s = int(math.floor(t - ((h * 3600) + (m * 60))))
            msg = 'You owe `{}` credits with a {}% interest rate per minute. You must return your loan in `{}` hours, `{}` minutes, and `{}` seconds or all your stats will be reset. You can return your loan at any time with `e!loan return`, as long as you have enough money to.'.format(self.calculate_loan(loans[str(ctx.author.id)]['principal'], loans[str(ctx.author.id)]['start']), int((Utils.LOANINTRATE - 1.0) * 100), h, m ,s)
        await ctx.send(msg)
        
    @loan.command(
        name = "return",
        description = "Returns the money you owe",
        aliases = ["r"],
        brief = "Returns the money you owe",
        help = "Gives back the money you borrowed for you loan."
)
    async def returnloan(self, ctx):
        with open('loans.json', 'r') as f:
            loans = json.load(f)
        if (not str(ctx.author.id) in loans) or (not loans[str(ctx.author.id)]['active']):
            msg = "You don't have a loan to return..."
        elif self.get_stats(ctx.author.id, 'credits') < self.calculate_loan(loans[str(ctx.author.id)]['principal'], loans[str(ctx.author.id)]['start']):
            msg = "You don't have enough money to pay off your loan!"
        else:
            current = self.calculate_loan(loans[str(ctx.author.id)]['principal'], loans[str(ctx.author.id)]['start'])
            msg = "You returned `{}` credits to the emu bank. Your loan is finished!".format(current)
            self.add_stats(ctx.author.id, -current, 'credits')
            del loans[str(ctx.author.id)]
            with open('loans.json', 'w') as f:
                json.dump(loans, f, sort_keys = False, indent = 4)
        await ctx.send(msg)
        
    @tasks.loop(seconds = 5)
    async def loan_check(self):
        await self.bot.wait_until_ready()
        try:
            with open('loans.json', 'r') as f:
                self.loans = json.load(f)
            for user_id in list(self.loans):
                now = int(time.time())
                loan = self.loans[user_id]
                if loan['time'] <= now:
                    current = self.calculate_loan(loan['principal'], loan['start'])
                    if self.get_stats(user_id, 'credits') > current:
                        self.add_stats(user_id, -current, 'credits')
                        msg = 'The time to return your loan is over, and the amount, `{}` credits, has automatically been collected from you.'.format(current)
                    else:
                        cred = self.get_stats(user_id, 'credits')
                        store = self.get_stats(user_id, 'storage')
                        defse = self.get_stats(user_id, 'defense')
                        self.add_stats(user_id, -cred, 'credits')
                        self.add_stats(user_id, -store, 'storage')
                        self.add_stats(user_id, -defse, 'defense')
                        msg = 'You have not returned your loan in time. All of your stats have been reset.'
                    del self.loans[str(user_id)]
                    with open('loans.json', 'w') as f:
                        json.dump(self.loans, f, sort_keys = False, indent = 4)
                    await self.bot.get_user(int(user_id)).send(msg)
        except Exception as e:
            print(e)
    
    @commands.command(
        name = "getcredits",
        aliases = ["gc"],
        hidden = True
)
    @commands.has_role('Tester')
    async def getcredits(self, ctx, numcredits: int):
        self.add_stats(ctx.author.id, numcredits, 'credits')
        msg = "Got `" + str(numcredits) + "` credits, tester!"
        await ctx.send(msg)
        
    @commands.command(
        name = "fillmeup",
        aliases = ["fill", "fillup", "fmu", "fm"],
        hidden = True
)
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
