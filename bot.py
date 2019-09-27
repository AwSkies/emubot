#imports stuff
import discord
import json
import os.path
import threading
import random
import asyncio

from cogs.masterclass import masterclass
from discord.ext import commands

#gives token -----------------------------------------------------------------
with open('TOKEN.txt', 'r') as f:
    TOKEN = f.readline()

class EmuBot(commands.bot, masterclass):
    def __init__(self):
        DESCRIPTION = '''A discord bot to honor our best friends, the emus. 
        With this bot you can use fun (and pointless) commands, earn credits by chatting, use those credits to buy emus, and use those emus to attack or defend against your friends.'''
        
        commands.bot.__init__(command_prefix = 'e!'
                             description = DESCRIPTION
                             case_insensitive = True)
        masterclass.__init__()
        
        self.COGS = ['cogs.fun', 'cogs.game']
        for cog in self.COGS:
            self.load_extension(cog)
            
    async def on_message(self, message):
        #spam protection to give credits or start timer -------------------------------
        if (not message.author.id in self.SPAMCATCH) or (message.author.id in self.SPAMCATCH and not self.SPAMCATCH[message.author.id]):
            add_stats(message.author.id, 10, 'credits')
            self.SPAMCATCH[message.author.id] = True
            def spamtimer():
                self.spamswitch(message.author.id)
            t = threading.Timer(10.0, spamtimer)
            t.start()
            
        await self.process_commands(message)
    
    async def on_command_error(ctx, error):
        await ctx.send(str(error))
        print(error)
    
    async def on_ready(self):
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')
        await self.change_presence(game=discord.Game(name= "Say e!help"))
        
    
#here are all the things triggered by messages -------------------------------
@client.event
async def on_message(message):

    #initial buy message ----------------------------------------------------------
    if message.content.upper () == 'E!BUY':
        if get_value(message.author.id, 'credits') < emuprice:
            val = get_value(message.author.id, 'credits')
            msg = "You have `{}` credits.\nAn emu costs `".format(val) + str(emuprice) + "` credits. You do not have enough credits to buy even one emu."
            await client.send_message(message.channel,msg)
        else:
            askedforbuyemu[message.author.id] = True
            val = get_value(message.author.id, 'credits')
            msg = '''You have `{}` credits.\nAn emu costs `'''.format(val) + str(emuprice) + '''` credits. If you would like to buy an emu, say yes, then the number of emus you would like to buy. (Ex. `yes 2`). Say no to cancel.'''.format(get_value(message.author.id, 'credits'))
            await client.send_message(message.channel, msg)

    #buying an emu after saying yes -----------------------------------------------
    if (message.author.id in askedforbuyemu) and askedforbuyemu[message.author.id] and (message.content.upper ().startswith('YES')): 
        args = message.content.split(" ")
        if len(args) == 1:
            msg = "To buy an emu, say yes then the amount of emus you would like to buy. (Ex. `yes 2`)"
            await client.send_message(message.channel, msg)
        else:
            numemus = intify(args[1])
            if numemus < 1 or len(args) > 2 or numemus + get_value(message.author.id, 'emustorage') + get_value(message.author.id, 'emudefense') > maxemus:
                if numemus < 1:
                    msg = "You can't buy less than one emu you trickster!"
                    await client.send_message(message.channel, msg)
                if len(args) > 2:
                    msg = "To buy an emu, just say yes then the number of emus you would like to buy. (Ex. `yes 2`)"
                    await client.send_message(message.channel, msg)
                if numemus + get_value(message.author.id, 'emustorage') + get_value(message.author.id, 'emudefense') > maxemus:
                    askedforbuyemu[message.author.id] = False
                    msg = "That is more than the maximum number of emus you can have! (" + str(maxemus) + ")"
                    await client.send_message(message.channel, msg)
            else:
                if numemus == 1:
                    askedforbuyemu[message.author.id] = False
                    user_add_value(message.author.id, -emuprice, 'credits')
                    user_add_value(message.author.id, 1, 'emustorage')
                    msg = '''You bought an emu! Use e!stats to see your stats'''
                    await client.send_message(message.channel, msg)
                else:
                    if get_value(message.author.id, 'credits') < emuprice * numemus:
                        askedforbuyemu[message.author.id] = False
                        val = get_value(message.author.id, 'credits')
                        msg = "You have `{}` credits.\nThe number of emus you want to buy cost `".format(val) + str(emuprice * numemus) + "` credits. You do not have enough credits to buy those emus."
                        await client.send_message(message.channel,msg)
                    else:
                        askedforbuyemu[message.author.id] = False
                        user_add_value(message.author.id, -(emuprice * numemus), 'credits')
                        user_add_value(message.author.id, (numemus), 'emustorage')
                        msg = '''You bought `''' + str(numemus) + '''` emus! Use e!stats to see your stats'''
                        await client.send_message(message.channel, msg)

    #saying no to buying an emu ---------------------------------------------------
    if (message.author.id in askedforbuyemu) and askedforbuyemu[message.author.id] and (message.content.upper () == 'NO'):
        askedforbuyemu[message.author.id] = False
        msg = "Canceled"
        await client.send_message(message.channel,msg)

    #initial reset message --------------------------------------------------------
    if message.content.upper () == 'E!RESET':
        askedforreset[message.author.id] = True
        msg = '''Are you sure you want to reset ***all*** of your stats? You'll lose everything! If you're sure, say yes. To cancel, say no.'''
        await client.send_message(message.channel, msg)

    #saying no to resetting -------------------------------------------------------
    if (message.author.id in askedforreset) and askedforreset[message.author.id] and (message.content.upper () == 'NO'):
        askedforreset[message.author.id] = False
        msg = "Canceled"
        await client.send_message(message.channel,msg)

    #reseting after saying yes ----------------------------------------------------
    if (message.author.id in askedforreset) and askedforreset[message.author.id] and (message.content.upper ().startswith('YES')): 
        askedforreset[message.author.id] = False
        user_add_value(message.author.id, -(get_value(message.author.id, 'credits')), 'credits')
        user_add_value(message.author.id, -(get_value(message.author.id, 'emustorage')), 'emustorage')
        user_add_value(message.author.id, -(get_value(message.author.id, 'emudefense')), 'emudefense')
        msg = "All of your stats have been reset."
        await client.send_message(message.channel,msg)

    #getcredits for testers -------------------------------------------------------
    if message.content.upper ().startswith('E!GETCREDITS'):
        if "448272810561896448" in [role.id for role in message.author.roles]:
            args = message.content.split(" ")
            if len(args) == 1 or len(args) > 2:
                if len(args) == 1:
                    msg = "To add credits, say e!getcredits then the amount of credits you would like to get. (Ex. `e!getcredits 600`)"
                    await client.send_message(message.channel, msg)
                if len(args) > 2:
                    msg = "To add credits, just say e!getcredits then the number of credits you would like to get. (Ex. `e!getcredits 600`)"
                    await client.send_message(message.channel, msg)
            else:
                numcredits = intify(args[1])
                user_add_value(message.author.id, numcredits, 'credits')
                msg = '''Got `''' + str(numcredits) + '''` credits, Tester!'''
                await client.send_message(message.channel, msg)
        else:
            msg = 'You do not have permission to use this command.'
            await client.send_message(message.channel, msg)

    if message.content.upper ().startswith("E!TEST"):
        print(message.mentions)

    #fills testers to a 20,000 credits, 15 emus in storage, and 5 emus on defense -
    if message.content.upper ().startswith('E!FILLMEUP'):
        if "448272810561896448" in [role.id for role in message.author.roles]:
            #sets credits to zero
            user_add_value(message.author.id, -get_value(message.author.id, 'credits'), 'credits')
            user_add_value(message.author.id, -get_value(message.author.id, 'emustorage'), 'emustorage')
            user_add_value(message.author.id, -get_value(message.author.id, 'emudefense'), 'emudefense')
            #adds amount of credits
            user_add_value(message.author.id, 20000, 'credits')
            user_add_value(message.author.id, maxemus - maxdefense, 'emustorage')
            user_add_value(message.author.id, maxdefense, 'emudefense')
            msg = 'You are maxed out, tester!'
            await client.send_message(message.channel, msg)
        else:
            msg = "You do not have permission to use this command!"
            await client.send_message(message.channel, msg)
            
    #putting emus on defense command ----------------------------------------------
    if message.content.upper ().startswith('E!DEFEND') or message.content.upper ().startswith('E!DEFENCE') or message.content.upper ().startswith('E!DEFENSE'):
        if get_value(message.author.id, 'emustorage') > 0:
            args = message.content.split(" ")
            if len(args) == 1:
                msg = "To put emus on defense, say e!defend then the amount of emus you would like to put on defense. (Ex. `e!defend 2`)"
                await client.send_message(message.channel, msg)
            else:
                numemus = intify(args[1])
                if get_value(message.author.id, 'emudefense') + numemus <= maxdefense:
                    if numemus < 1 or len(args) > 2:
                        if numemus < 1:
                            msg = "You can't put less than one emu on defense you trickster!"
                            await client.send_message(message.channel, msg)
                        if len(args) > 2:
                            msg = "To put an emu on defense, just say e!defend then the number of emus you would like to put on defense. (Ex. `e!defend 2`)"
                            await client.send_message(message.channel, msg)
                    else:
                        if numemus == 1:
                            user_add_value(message.author.id, -1, 'emustorage')
                            user_add_value(message.author.id, 1, 'emudefense')
                            msg = '''One emu added to defense! Remember you can check your stats with e!stats!'''
                            await client.send_message(message.channel, msg)
                        else:
                            user_add_value(message.author.id, -numemus, 'emustorage')
                            user_add_value(message.author.id, numemus, 'emudefense')
                            msg = "`" + str(numemus) + "` emus added to defense! Remember you can check your stats with e!stats!"
                            await client.send_message(message.channel, msg)
                else:
                    msg = '''That number of emus would go over the maximum amount of emus on defense! (5)'''
                    await client.send_message(message.channel, msg)
        else:
            msg = '''You have no emus to put on defense! Remember, you can buy emus with e!buy!'''
            await client.send_message(message.channel, msg)

    #taking emus off defense command ----------------------------------------------
    if message.content.upper ().startswith('E!OFFDEFENSE') or message.content.upper ().startswith('E!OFFDEFENCE'):
        if get_value(message.author.id, 'emudefense') > 0:
            args = message.content.split(" ")
            if len(args) == 1:
                msg = "To take an emu off defense, say e!offdefense then the amount of emus you would like to take off defense. (Ex. `e!offdefense 2`)"
                await client.send_message(message.channel, msg)
            else:
                numemus = intify(args[1])
                if get_value(message.author.id, 'emudefense') - numemus >= 0:
                    if numemus < 1 or len(args) > 2:
                        if numemus < 1:
                            msg = "You can't take less than one emu off defense you trickster!"
                            await client.send_message(message.channel, msg)
                        if len(args) > 2:
                            msg = "To take an emu off defense, just say e!offdefense then the number of emus you would like to take off defense. (Ex. `e!offdefense 2`)"
                            await client.send_message(message.channel, msg)
                    else:
                        if numemus == 1:
                            user_add_value(message.author.id, -1, 'emudefense')
                            user_add_value(message.author.id, 1, 'emustorage')
                            msg = '''One emu taken off defense! Remember you can check your stats with e!stats!'''
                            await client.send_message(message.channel, msg)
                        else:
                            user_add_value(message.author.id, -numemus, 'emudefense')
                            user_add_value(message.author.id, numemus, 'emustorage')
                            msg = "`" + str(numemus) + "` emus taken off defense! Remember you can check your stats with e!stats!"
                            await client.send_message(message.channel, msg)
                else:
                    msg = '''That number of emus would make you have negative emus! Remember, you can buy emus with e!buy and put them on defense with e!defend (number of emus you want to put on defense)!'''
                    await client.send_message(message.channel, msg)
        else:
            msg = '''You have no emus to take off defense! Remember, you can buy emus with e!buy and put them on defense with e!defend (number of emus you want to put on defense)!'''
            await client.send_message(message.channel, msg)
    
    #attack command ---------------------------------------------------------------
    if message.content.upper ().startswith('E!ATTACK'):
        args = message.content.split(" ")
        if not "448272810561896448" in [role.id for role in message.author.roles]:
            if (message.author.id in attacktimer1) and (attacktimer1[message.author.id]):
                msg = "You can't attack yet!"
                await client.send_message(message.channel, msg)
                return
        #checks for improper format
        if len (args) == 1 or len (args) == 2 or len (args) >= 4:
            msg = '''Say how many emus you would like to attack with and the person you would like to attack. Ex. e!attack [number] [@person]'''
            await client.send_message(message.channel, msg)
        else:
            emuattacknum = intify(args[1])
            #checks if user has emus at all 
            if get_value(message.author.id, 'emustorage') == 0:
                msg = '''You have no emus to attack with! Remember, you can buy emus with e!buy!'''
                await client.send_message(message.channel, msg)
            #checks if the number you are trying to attack with is negative
            elif emuattacknum <= 0:
                msg = "You can't put less than one emu on attack!"
                await client.send_message(message.channel, msg)
            #makes sure it is within the limit of emus on attack
            elif emuattacknum > maxattack:
                msg = '''That's more than you are allowed to send on attack. (''' + str(maxattack) + ')'
                await client.send_message(message.channel, msg)
            #checks if user has enough emus
            elif emuattacknum > get_value(message.author.id, 'emustorage'):
                msg = 'You are trying to attack with more emus that you have in your storage, you silly emu warlord!'
                await client.send_message(message.channel, msg)
            #gets uid
            #uidstr = the string version of the uid (Ex. <@!213676807651255>)
            else:
                uidstr = args[2][2:-1]
                #checks if uid has a !
                if uidstr[0] == '!':
                    uidstr = uidstr[1:]
                if uidstr == client.user.id:
                    msg = '''You can't attack me!!!'''
                    await client.send_message(message.channel, msg)
                elif uidstr == message.author.id:
                    msg = '''You can't attack yourself!'''
                    await client.send_message(message.channel, msg)
                else:
                    prebattlecredits = get_value(uidstr, 'credits')
                    creditcalnum = 700*(emuattacknum - get_value(uidstr, 'emudefense'))
                    #checks if user broke other user's defenses
                    if creditcalnum < 0:
                        user_add_value(uidstr, -emuattacknum, 'emudefense')
                    else: #if user broke other user's defenses
                        #checks if user being attacked can pay attackee
                        if prebattlecredits - creditcalnum < 0:
                            user_add_value(message.author.id, prebattlecredits, 'credits')
                            user_add_value(uidstr, -prebattlecredits, 'credits')
                        else: 
                            user_add_value(message.author.id, creditcalnum, 'credits')
                            user_add_value(uidstr, -creditcalnum, 'credits')
                        user_add_value(uidstr, -get_value(uidstr, 'emudefense'), 'emudefense')
                    user_add_value(message.author.id, -emuattacknum, 'emustorage')
                    if not "448272810561896448" in [role.id for role in message.author.roles]:
                        def inattacktimer():
                            attacktimer(message.author.id)
                        attacktimer1[message.author.id] = True
                        t = threading.Timer(14400.0, inattacktimer)
                        t.start()
                    msg = '<@' + uidstr + '> was attacked by {0.author.mention} with `'.format(message) + str(emuattacknum) + '` emus and now has `{}` emus left on defense, '.format(get_value(uidstr, 'emudefense')) + '{0.author.mention} stole `'.format(message) + str(creditcalnum) + '` credits.'
                    await client.send_message(message.channel, msg)
                    
    #easter egg -------------------------------------------------------------------
    if message.content.upper () == 'E!EASTEREGG':
        msg = 'You found the Easter Egg! You get 1 credit.'
        await client.send_message(message.channel, msg)
        user_add_value(message.author.id, 1, 'credits')
        
    #help commands ----------------------------------------------------------------
    if message.content.upper () == 'E!HELP':
        embed=discord.Embed(title="How to use the Emu Bot", url="https://sites.google.com/view/emu-bot-habitat/commands")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/445349891217031179/541704664236687361/imageedit_1_8656546600.png")
        embed.add_field(name='Helpful Commands', value='Gives helpful info about the bot, emus, and more.', inline=False)
        embed.add_field(name='Game Commands', value='Commands related to the Emu Bot game.', inline=True)
        embed.add_field(name='Fun Commands', value='Just for fun, these commands usually show silly pictures or videos of emus.', inline=True)
        embed.add_field(name='Miscellaneous Commands', value="Could be anything. Mostly just commands that don't really fit into any category.", inline=True)
        embed.add_field(name='Additional Info', value='For help with each category, just say e!help (category) (Ex: e!help fun) (Note: When using help for miscellaneous commands, just say e!help misc) Also remember, you can suggest more commands in the Emu Bot testing and support server!', inline=True)
        embed.set_footer(text="Emu Bot created and programmed by @CaptainClumsy#3018")
        await client.send_message(message.channel, embed=embed)

    if message.content.upper () == 'E!HELP MISC':
        embed=discord.Embed(title='Miscellaneous Commands', description='''**Could be anything. Mostly just commands that don't really fit into any category.**
e!say: Emu Bot will say what you put after the e!say''', color=0x00ff00)
        await client.send_message(message.channel, embed=embed)

    if message.content.upper () == 'E!HELP GAME':
        embed=discord.Embed(title='Game Help & Commands', description='''**In the emu bot game, you gain credits by participating in chat. You can spend these credits on emus and attack your friends with them.**
e!help game explain: Goes more in-depth about the emu game
e!stats: Shows your credits, emus in storage, and emus on defense
e!buy: Lets you buy emus
e!defend `(number)`: Puts `(number)` emus on defense
e!offdefense `(number)`: Takes `(number)` emus off defense
e!attack `(number)` @`(person)`: Attacks `(person)` with `(number)` emus
e!loan `(number)`: Gives you a loan of `(number)` credits with an interest rate of 1% per minute and (time undecided) *WIP*
e!gamble `(number1)` `(number2)`: Gambles `(number1)` credits, allowing you to choose from `(number2)` numbers, the first number always being one. If you choose the correct number, you will receive `(number1)` times half of `(number2)` credits. *WIP*
e!give `(number)` `@person`: Gives `@person` `number` credits *WIP*
e!reset: Resets ***all*** of your stats''', color=0x00ff00)
        await client.send_message(message.channel, embed=embed)

    if message.content.upper () == 'E!HELP GAME EXPLAIN':
        embed=discord.Embed(title='Game Explanation', description='''**In the emu bot game, you gain credits by participating in chat. You can spend these credits on emus and attack your friends with them.**
-You earn credits by sending messages.
-You can use those credits to buy emus
-The maximum amount of emus you can have is 20 emus
-You can put emus on defense
-The maximum amount of emus on defense is 5 emus
-You can also use emus to attack your friends
-The maximum amount of emus you can attack with at a time is 10 emus
The amount of emus you attack someone with that go over the amount of emus they have on defense grants you 700 credits for each emu.''', color=0x00ff00)
        await client.send_message(message.channel, embed=embed)
        
    #say command ------------------------------------------------------------------
    if message.content.upper ().startswith ('E!SAY'):
        args = message.content.split(" ")
        if len(args) == 1:
            msg = '''To use this command, put something after the e!say'''
            await client.send_message(message.channel, msg)
        else:
            await client.send_message(message.channel, "%s" % (" ".join(args[1:])))

    #changing game status (for me only) -------------------------------------------
    if message.content.upper ().startswith('E!CHANGESTATUS'):
        if message.author.id == "369267862050832385":
            args = message.content.split(" ")
            if len (args) == 1:
                msg = '''Status changed to Say e!help'''
                await client.change_presence(game=discord.Game(name= "Say e!help"))
                await client.send_message(message.channel, msg)
            else:
                msg = '''Status changed to '''  '%s' % (" ".join(args[1:]))
                await client.change_presence(game=discord.Game(name='%s' % (" ".join(args[1:]))))
                await client.send_message(message.channel, msg)
        else:
            msg = 'You do not have permission to use this command.'
            await client.send_message(message.channel, msg)

#runs the bot -------------------------------------------------------------
if __name__ == '__main__':
    b = EmuBot()
    b.run(TOKEN)
