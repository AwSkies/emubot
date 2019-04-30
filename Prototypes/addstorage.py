    #addstorage command------------------------------------------
    if message.content.upper ().startswith("E!ADDSTORAGE"):
        askedforaddstorage[message.author.id] = True
        await client.send_message(message.channel, msg)
        
    #saying no to adding storage
    if (message.author.id in askedforaddstorage) and askedforaddstorage[message.author.id] and (message.content.upper () == 'NO'):
        askedforaddstorage[message.author.id] = False
        msg = "Canceled"
        await client.send_message(message.channel,msg)
        
    #adding storage after saying yes
    if (message.author.id in askedforaddstorage) and askedforaddstorage[message.author.id] and (message.content.upper () == 'YES'): 
        askedforaddstorage[message.author.id] = False
        ?
        msg = "Emu storage increased by ?"
        await client.send_message(message.channel,msg)
