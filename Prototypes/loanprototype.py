    #loan command------------------------------------------
    if message.content.upper ().startswith == "E!LOAN":
        args = message.content.split(" ")
        numcreds = intify(args[1])
        if (len(args) < 2) or (len(args) > 2):
            msg = "Say e!loan `number` `@person` to give `@person` `number` credits!"
            await client.send_message(message.channel, msg)
        elif numcreds < 1:
            msg = "You can't loan lessa than one credit!"
            await client.send_message(message.channel, msg)
        elif numcreds > get_value(message.author, 'credits':
            msg = "You can't loan lessa than one credit!"
            await client.send_message(message.channel, msg)
        else:
            uidstr = args[2][2:-1]
            #checks if uid has a !
            if uidstr[0] == '!':
                uidstr = uidstr[1:]
            if uidstr == client.user.id:
                msg = "You can't loan me credits!!!"
                await client.send_message(message.channel, msg)
            elif uidstr == message.author.id:
                msg = "You can't loan yourself credits!"
                await client.send_message(message.channel, msg)
            else:
                user_add_value(message.author.id, -numcreds, 'credits')
                user_add_value(uidstr, numcreds, 'credits')
                msg = "{0.author.mention} loaned".format(message) + "<@" + uidstr + "> `{}` credits!".format(str(numcreds))
                await client.send_message(message.channel, msg)
