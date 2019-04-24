import datetime

    #loan command -----------------------------------------------------------------
    if message.content.upper ().startswith("E!LOAN"):
        args = message.content.split(" ")
        principal = intify(args[1])
        if len(args) == 1 or len(args) > 2:
            msg = 'To take out a loan, say e!loan `number` to be loaned `number` credits.'
            await client.send_message(message.channel, msg)
        elif principal < 1:
            msg =
        else:
            with open('loans.json', 'r') as f:
                loans = json.load(f)
            if loans[message.author.id] == True:
                msg = "You already have a loan, and you can't get two at once! If you want to pay it off, say e!returnloan."
                await client.send_message(message.channel, msg)
            else:
                loantime = (int(datetime.datetime.now().strftime('%d')) * 1440) + int(datetime.datetime.now().strftime('%H') * 60) + int(datetime.datetime.now().strftime('%H')
                loaninfo = {message.author.id: {}}
                loaninfo[message.author.id]['time'] = loantime
                loaninfo[message.author.id]['principal'] = principal
                if os.path.isfile('loans.json'):
                    loan = loaninfo[message.author.id]
                    with open('loans.json', 'w') as fp:
                        json.dump(loan, fp, sort_keys = True, indent = 4)
                else:
                    something
                user_add_value(message.author.id, <principal>, 'credits')
                msg = 'You were loaned <principal> credits with a <tbdintrest> intrest rate! You must return it by '
                await client.send_message(message.channel, msg)
    
    if message.content.upper () == 'E!RETURNLOAN':
        try:
            with open('loans.json', 'r') as fp:
                loan = json.load(fp)
                loaninfo = loan[message.author.id]
                principal = loaninfo['principal']
                time = loaninfo['time']
            time -= (int(datetime.datetime.now().strftime('%d')) * 1440) + int(datetime.datetime.now().strftime('%H') * 60) + int(datetime.datetime.now().strftime('%H')
            if not loaninfo[message.author.id] == None
                loancalnum = principal * <rate> * time
                loaninfo[message.author.id] = None
                with open('loans.json', 'w') as f:
                    json.dump(loaninfo, f, sort_keys = True, indent = 4)
                if not get_value(message.author.id, 'credits') - principal < 0:
                    user_add_value(message.author.id, principal, 'credits')
                    msg = 'You returned your loan for `{}` credits!'.format(loancalnum)
                    await client.send_message(message.channel, msg)
                
            else:
                msg = "You don't have a loan to return!"
                await client.send_message(messsage.channel, msg)
        except KeyError:
            msg = "You don't have a loan to return!"
            await client.send_message(messsage.channel, msg)
