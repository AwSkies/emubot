    if message.content.upper ().startswith == 'E!ATTACK':
        args = message.content.split(" ")
        emuattacknum = intify(args[1])
##checks for improper format
        if len (args) == 1 or len (args) == 2 or len (args) >= 4:
            msg = '''Say how many emus you would like to attack with and the person you would like to attack. Ex. e!attack [number] [@person]'''
            await client.send_message(message.channel, msg)
## checks if user has emus at all 
        elif get_value(message.author.id, 'emustorage') == 0:
            msg = '''You have no emus to attack with! Remember, you can buy emus with e!buy!'''
            await client.send_message(message.channel, msg)
##makes sure it is within the limit of emus on attack
        elif emuattacknum > maxattack:
            msg = '''That's more than you are allowed to send on attack.'''
            await client.send_message(message.channel, msg)
##checks if user has enough emus
        elif emuattacknum > get_value(message.author.id, 'emustorage'):
            msg = 'You are trying to attack with more emus that you have in your storage, you silly emu warlord!'
##gets uid
##uidstr = the string version of the uid (Ex. <@!213676807651255>)
        else:
            uidstr = args[2][2:-1]
##checks if uid has a !
            if uidstr[0] == '!':
                uidstr = uidstr[1:]
##intifies uid
            uid = intify(uidstr)
            prebattlecredits = get_value(uid, 'credits')
            creditcalnum = 700*(emuattacknum - get_value(uid, 'emudefense'))
##checks if user broke other user's defenses
            if creditcalnum < 0:
                user_add_value(uid, -emuattacknum, 'emudefense')
##checks if user being attacked can pay attackee
            elif prebattlecredits - creditcalnum < 0:
                user_add_value(message.author.id, prebattlecredits, 'credits')
                user_add_value(uid, -prebattlecredits, 'credits')
            else: 
                user_add_value(message.author.id, creditcalnum, 'credits')
                user_add_value(uid, -creditcalnum, 'credits')
##charges user the emus they are using to attack
            msg = '<@' + str(uid) + '> was attacked by {0.author.mention} with `'.format(message) + str(emuattacknum) + '` emus, and now has `{}` emus left on defense '.format(get_value(uid, 'emus')) + 'and `{}` credits left'.format(get_value(uid, 'emustorage'))
            await client.send_message(message.channel, msg)


##                        if emuattacknum >= get_value(uid, 'emudefense'):
##                            user_add_value(uid, -get_value(uid, 'emudefense'), 'emudefense')
##                            creditcalnum = 1000*(emuattacknum - maxdefense)
##                            user_add_value(message.author.id, creditcalnum, 'credits')
##                            if get_value(uid, 'credits') - creditcalnum < 0:
##                                    user_add_value(uid, -get_value(uid, 'credits'), 'credits')
##                                else:
##                                    user_add_value(uid, -creditcalnum)
##                        else:
##                            if get_value(uid, emudefense) == 0:
##                                creditcalnum = 1000*emuattacknum
##                                user_add_value(message.author.id, creditcalnum, 'credits')
##                                if get_value(uid, 'credits') - creditcalnum < 0:
##                                    user_add_value(uid, -get_value(uid, 'credits'))
##                                else:
##                                    user_add_value(uid, -creditcalnum)
