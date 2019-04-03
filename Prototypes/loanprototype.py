import datetime

loanstarted = dict()

global loanstarted

    #loan command------------------------------------------
    if message.content.upper () == "E!LOAN":
        if loanstarted[message.author.id] == True:
            msg = "You already have a loan, and you can't get two at once! If you want to pay it off, say e!returnloan."
            await client.send_message(message.channel, msg)
        else:
            loanstarttime = dict()
            loanstarttime[message.author.id] = int(datetime.datetime.today().strftime('%j'))
            if os.path.isfile('loans.json'):
                loan = loanstarttime[message.author.id]
                with open('loans.json', 'w') as fp:
                    json.dump(loan, fp, sort_keys = True, indent = 4)
                #maybe put a KeyError thing here
            else:
                something
            loanstarted[message.author.id] = True
            user_add_value(message.author.id, <principal>, 'credits')
            msg = 'You were loaned <principal> credits with a <tbdintrest> intrest rate!'
            await client.send_message(message.channel, msg)
    
    if message.content.upper () == 'E!RETURNLOAN':
        if loanstarted[message.author.id] == True:
            with open('loans.json', 'r') as fp:
                loan = json.load(fp)
                loantime = loan[message.author.id]
            t = loantime
            loancalnum = <principal> * <rate> * t
        else:
            msg = 'You have no loan to repay!'
            await client.send_message(message.author, msg)
