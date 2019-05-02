#in bot.py as of commit 89dc5d1, change all instances of maxemus to maxemus[message.author.id]
#for changing of line #20 of bot.py as of commit 89dc5d1
MAXEMUSDEFAULT = 20
#
    
    #for insertion in global section
    global maxemus
    
    #gets maxemus from json file and sets maxemus to correct value
    with open('maxemus.json', 'r') as f:
        maxemus = json.load(f)
        if not message.author.id in maxemus:
            maxemus[message.author.id] = MAXEMUSDEFAULT
    
    #addstorage command------------------------------------------
    if message.content.upper ().startswith("E!ADDSTORAGE"):
        askedforaddstorage[message.author.id] = True
        msg = 'If you want to add storage, say yes, then the number you want to increase your storage by. (Ex. yes 5) To cancel, say no.'
        await client.send_message(message.channel, msg)
        
    #saying no to adding storage
    if (message.author.id in askedforaddstorage) and askedforaddstorage[message.author.id] and (message.content.upper () == 'NO'):
        askedforaddstorage[message.author.id] = False
        msg = "Canceled"
        await client.send_message(message.channel,msg)
        
    #adding storage after saying yes
    if (message.author.id in askedforaddstorage) and askedforaddstorage[message.author.id] and (message.content.upper () == 'YES'): 
        args = message.content.split(" ")
        numei = intify(args[1])
        if len(args) < 2 or len(args) > 2:
            msg = "To increase your storage, say yes, then the number you want to increase your storage by. (Ex. yes 5) To cancel, say no."
            await client.send_message(message.channel, msg)
        else:
            askedforaddstorage[message.author.id] = False
            maxemus[message.author.id] += numei
            with open('maxemus.json', 'w') as f:
                json.dump(maxemus, f, sort_keys = True, indent = 4)
            msg = "Emu storage increased by `{}`.".format(numei)
            await client.send_message(message.channel,msg)
