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
    self.MAXEMUSDEFAULT = 20 #this line will replace MAXEMNUS
    self.ADDSTORAGEPRICE = 5000
    self.ASKEDFORADDSTORAGE = dict()
    
    #for insertion in masterclass.py function section:
    def get_maxemus(self, ctx):
        with open('maxemus.json', 'r') as f:
            maxemus = json.load(f)
            if not ctx.author.id in maxemus:
                maxemus[ctx.author.id] = self.MAXEMUSDEFAULT
        return maxemus
    #change every instance of self.MAXEMUS to a variable defined at the beginning of the command
    
    #addstorage commmand discord.py rewrite---------------------
    @commands.group(name = "addstorage",
                    description = "Increases your max emu storage",
                    aliases = ['as', 'adds'],
                    brief = "Increases your max emu storage",
                    help = "???.",
                    usage = "e!addstorage",
                    case_insensitive = True,
                    invoke_without_command = True
)
    async def addstorage(self, ctx):
        val = self.get_stats(ctx.author.id, 'credits')
        msg = "You have `{}` credits.\nIncreasing your max storage costs `{}` credits. ".format(val, self.ADDSTORAGEPRICE)
        if val < self.ADDSTORAGEPRICE:
            msg += "You do not have enough credits to increase your storage."
        else:
            self.ASKEDFORADDSTORAGE[ctx.author.id] = True
            msg += "If you would like to increase your storage, say e!addstorage yes. If you want to cancel, say e!addstorage no."
        await ctx.send(msg)
        
    @addstorage.command(name = "yes",
                        aliases = ["y"],
                        hidden = True
)
    async def addstorageconfirm(self, ctx):
        maxemus = self.get_maxemus(ctx)
        if not ctx.author.id in self.ASKEDFORADDSTORAGE or not self.ASKEDFORADDSTORAGE[ctx.author.id]:
            msg = "You didn't ask to add storage yet! Use e!addstorage if you would like to."
        elif get_stats(ctx.author.id, 'credits') < self.ADDSTORAGEPRICE:
            msg = "You don't have enough credits to buy another storage slot."
        else:
            self.add_stats(ctx.author.id, -self.ADDSTORAGEPRICE, 'credits')
            self.ASKEDFORADDSTORAGE[ctx.author.id] = False
            maxemus[ctx.author.id] += 1
            with open('maxemus.json', 'w') as f:
                json.dump(maxemus, f, sort_keys = True, indent = 4)
            msg = "Maximum emu storage increased by 1."
        await ctx.send(msg)
            
        
    @addstorage.command(name = "no",
                        aliases = ['n'],
                        hidden = True
)
    async def addstoragecancel(self, ctx):
        if not ctx.author.id in self.ASKEDFORADDSTORAGE or not self.ASKEDFORADDSTORAGE[ctx.author.id]:
            msg = "You didn't ask to add storage yet! Use e!addstorage if you would like to."
        else:
            msg = 'Canceled'
            self.ADDSTORAGE[ctx.author.id] = False
        await ctx.send(msg)
