#in bot.py as of commit 89dc5d1, change all instances of maxemus to maxemus[message.author.id]
#for changing of line #20 of bot.py as of commit 89dc5d1
MAXEMUSDEFAULT = 20
ADDSTORAGEPRICE = 5000
#
    
    #for insertion in global section
    #global MAXEMUSDEFAULT
    #global ADDSTORAGEPRICE
    
    #gets maxemus from json file and sets maxemus to correct value
    with open('maxemus.json', 'r') as f:
        maxemus = json.load(f)
        if not message.author.id in maxemus:
            maxemus[message.author.id] = MAXEMUSDEFAULT
    
    #addstorage command------------------------------------------
    if message.content.upper ().startswith("E!ADDSTORAGE"):
        askedforaddstorage[message.author.id] = True
        msg = 'If you want to add storage, say yes, then the number you want to increase your storage by. (Ex. yes 5) One more emu to store costs ' + ADDSTORAGEPRICE + ' credits. To cancel, say no.'
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
        price = numei * MAXEMUSDEFAULT
        if len(args) < 2 or len(args) > 2:
            msg = "To increase your storage, say yes, then the number you want to increase your storage by. (Ex. yes 5) To cancel, say no."
            await client.send_message(message.channel, msg)
        elif numei < 1:
            msg = "You can't add less than 1 emu to your storage!"
            await client.send_message(message.channel, msg)
        elif price > get_value(message.author.id, 'credits'):
            msg = 'You do not have enough credits to buy that many emus!'
            await client.send_message(message.channel, msg)
        else:
            askedforaddstorage[message.author.id] = False
            maxemus[message.author.id] += numei
            with open('maxemus.json', 'w') as f:
                json.dump(maxemus, f, sort_keys = True, indent = 4)
            msg = "Emu storage increased by `{}`.".format(numei)
            await client.send_message(message.channel,msg)
    
    #for insertion in masterclass.py variable section:
    self.MAXEMUSDEFAULT = 20
    self.ADDSTORAGEPRICE = 5000
    
    #addstorage commmand discord.py rewrite---------------------
    @commands.group(name = "addstorage",
                    description = "Increases your max emu storage",
                    aliases = ['as', 'adds'],
                    brief = "Increases your max emu storage",
                    help = "???.",
                    usage = "e!addstorage"
)
    
    async def addstorage(self, ctx):
        val = self.get_stats(ctx.author.id, 'credits')
        if val < self.ADDSTORAGEPRICE:
            msg = "You have `{}` credits.\nIncreasing your max storage costs `".format(val) + str(self.ADDSTORAGEPRICE) + "` credits. You do not have enough credits to increase your storage."
        else:
            self.ASKEDFORADDSTORAGE[ctx.author.id] = True
            msg = '''You have `{}` credits.\nIncreasing your max storage costs `".format(val) + str(self.ADDSTORAGEPRICE) + "` credits. If you would like to increase your storage, say e!addstorage yes.'''
        await ctx.send(msg)
        
        @buy.command(name = "yes",
                 aliases = ["y"],
                 hidden = True
)
        
    async def addstorageconfirm(self, ctx):
        if not (ctx.author.id in self.ASKEDFORADDSTORAGE and self.ASKEDFORADDSTORAGE[ctx.author.id]):
            msg = "You did not ask to increase your storage yet..."
        else:
