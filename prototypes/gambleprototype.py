#for insertion in dictonary section
gamblesetup = dict()
gamble_range_storage = dict()
gamblecreds = dict()

    #for insertion in global section
    global gamblesetup
    global gamble_range_storage
    global gamblecreds

    #gamble command----------------------------------------------------------------
    if message.content.upper ().startswith("E!GAMBLE"):
        args = message.content.split
        numcreds = intify(args[1])
        gamblerange = intify(args[2])
        #checks if the number of credits gambled is less than or equal to zero
        if numcreds > get_value(message.author.id, 'credits'):
            msg = "You don't have that number of credits to gamble!"
            await client.send_message(message.channel, msg)
          #checks is user has that many credits to gamble
        elif numcreds <= 0:
            msg = "You can't gamble that number of credits!"
            await client.send_message(message.channel, msg)
        elif gamblerange < 1:
            msg = "You can't pick from that amount of numbers!"
            await client.send_message(message.channel, msg)
        else:
            msg = 'Pick a number between 1 and {}. If you wish to cancel, say "cancel".'.format(gamblerange)
            await ctx.send(msg)
            gamblesetup[message.author.id] = True
            gamble_range_storage[message.author] = gamblerange
            gamblecreds[message.author.id] = numcreds
            with open('loans.json', 'w') as fp:
                json.dump(self.LOANS, fp, sort_keys=True, indent=4)

    if gamblesetup[message.author.id] == True:
        gamblerange = gamble_range_storage[message.author.id]
        numcreds = gamblecreds[message.author.id]
        args = message.content.split(" ")
        guessnum = args[1]
        try:
            guessnum = int(guessnum)
            if guessnum < 1:
                msg = "You can't guess a number less than 1!"
                await client.send_message(message.channel, msg)
            elif guessnum > gamblerange:
                msg = 'Pick a number between 1 and ' + str(gamblerange) + '''. If you wish to cancel, say "cancel".'''
                await client.send_message(message.channel, msg)
            else:
                def dicepicker():
                    dicenum = random.randint(1,6)
                    if dicenum == 1:
                        diceface = '<:dice1:559092222545625089>'
                    elif dicenum == 2:
                        diceface = '<:dice2:559092223044485140>'
                    elif dicenum == 3:
                        diceface = '<:dice3:559092223040552970>'
                    elif dicenum == 4:
                        diceface = '<:dice4:559092222935564301>'
                    elif dicenum == 5:
                        diceface = '<:dice5:559092223052873739>'
                    elif dicenum == 6:
                        diceface = '<:dice6:559092223145279491>'
                    return(diceface)
                gamble = random.randint(1,gamblerange)
                #losing outcome
                if gamble != guessnum:
                    outcome = 'lost'
                    user_add_value(message.author.id, -numcreds, "credits")
                else:
                #winning outcome
                    outcome = 'won'
                    credcalnum = numcreds * int(gamblerange / 2)
                    user_add_value(message.author.id, credcalnum, 'credits')
                msg = 'Rolling the dice...' + dicepicker() + dicepicker()
                edit = await client.send_message(message.channel, msg)
                await asyncio.sleep(1)
                edited = 'Rolling the dice...' + dicepicker() + dicepicker()
                await client.edit_message(edit, edited)
                await asyncio.sleep(1)
                edited = 'Rolling the dice...' + dicepicker() + dicepicker()
                await client.edit_message(edit, edited)
                await asyncio.sleep(1)
                #makes outcome
                if outcome == 'lost': 
                    edited = 'You lost, sorry... :('
                    await client.edit_message(edit, edited) 
                elif outcome == 'won':
                    edited = 'You won! you gained ' + str(credcalnum) + ' credits!'
                    await client.edit_message(edit, edited)
                gamblesetup[message.author.id] = False
                
        except ValueError:
            
            if message.content.upper () == "CANCEL":
                msg = 'Canceled'
                await client.send_message(message.author, msg)
            
            else:
                msg = 'Pick a number between 1 and ' + str(gamble_range_storage[message.author.id]) + '. If you wish to cancel, say "cancel".'
                await client.send_message(message.channel, msg)
                
    #gamble commmand discord.py rewrite-------------------------
    #for insertion in __init__ of masterclass in masterclass.py
        self.GAMBLEINFO = dict()
    #
    @commands.group(name = "gamble",
                    description = "Let's roll the dice...",
                    aliases = ["g"],
                    brief = "Gambles your credits (or your life) away...",
                    help = "[Insert explanation of the math of the gamble command here]",
                    usage = "e!gamble [number of credits to gamble] [number of ]"
                    invoke_without_command = True
                    case_insensitive = True
)
    async def gamble(self, ctx, numcreds: int, gamblerange: int):
        if numcreds > self.get_stats(ctx.author.id, 'credits'):
            msg = "You don't have that number of credits to gamble!"
        elif numcreds < 1:
            msg = "You can't gamble less than one credit!"
        elif gamblerange < 1:
            msg = "You can't pick from less than one!"
        else:
            msg = 'Pick a number between 1 and {}. If you wish to cancel, say "cancel".'.format(gamblerange)
            self.GAMBLEINFO = {ctx.author.id: {}}
            self.GAMBLEINFO[ctx.author.id]['started'] = True
            self.GAMBLEINFO[ctx.author.id]['range']   = gamblerange
            self.GAMBLEINFO[ctx.author.id]['credits'] = numcreds
        await ctx.send(msg)
    
    @gamble.command(name = "guess",
                    description = "Used to guess a number out of the range you specified using the gamble command",
                    aliases = ['g'],
                    brief = "Used to guess a number",
                    help = "Used to guess a number out of the range you specified using the gamble command. You must have previously specified the number of credits and the range.",
                    usage = 'e!gamble guess [number]'
)
    async def gambleguess(self, ctx, guessnum: int):
        gamblerange = self.GAMBLEINFO[ctx.author.id]['range']
        numcreds = self.GAMBLEINFO[ctx.author.id]['credits']
        if not self.GAMBLEINFO[ctx.author.id]['started'] or not ctx.author.id in self.GAMBLEINFO:
            msg = "You haven't made a gamble yet! Use e!gamble if you wish to."
            await ctx.send(msg)
        elif guessnum < 1 or guessnum > gamblerange:
            msg = 'Pick a number between 1 and {}. If you wish to cancel, use e!gamble cancel.'.format(gamblerange)
            await ctx.send(msg)
        else:
            num = random.randint(1, gamblerange)
            def dicepicker():
                dicenum = random.randint(1, 6)
                if dicenum == 1:
                    diceface = '<:dice1:559092222545625089>'
                elif dicenum == 2:
                    diceface = '<:dice2:559092223044485140>'
                elif dicenum == 3:
                    diceface = '<:dice3:559092223040552970>'
                elif dicenum == 4:
                    diceface = '<:dice4:559092222935564301>'
                elif dicenum == 5:
                    diceface = '<:dice5:559092223052873739>'
                elif dicenum == 6:
                    diceface = '<:dice6:559092223145279491>'
                msg = 'Rolling the dice...' + diceface + diceface
                return(msg)
            msg = await ctx.send(dicepicker())
            await asyncio.sleep(1.0)
            for range(2):
                await msg.edit(content = dicepicker())
                await asyncio.sleep(1.0)
            if not num == guessnum:
                self.add_stats(ctx.author.id, -numcreds, "credits")
                await msg.edit(content = 'Sorry, the number was `{}`. You lost `{}` credits... :('.format(num, numcreds))
            else:
                credcalnum = numcreds * int(gamblerange / 2)
                self.add_stats(ctx.author.id, credcalnum, 'credits')
                await msg.edit(content = ':confetti_ball: You won!!! You gained `{}` credits! :woohoo:'.format(credcalnum)
        
    @gamble.command(name = "cancel",
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
