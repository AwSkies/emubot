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
            msg = 'Pick a number between 1 and ' + str(gamblerange) + '''. If you wish to cancel, say "cancel".'''
            await client.send_message(message.channel, msg)
            gamblesetup[message.author.id] = True
            gamble_range_storage[message.author] = gamblerange
            gamblecreds[message.author.id] = numcreds

    if gamblesetup[message.author.id] == True:
        gamblerange = gamble_range_storage[message.author.id]
        numcreds = gamblecreds[message.author.id]
        args = message.content.split(" ")
        guessnum = args[0]
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
