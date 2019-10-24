import datetime

LOAN_INTEREST_RATE = 1.01 #per minute

    global LOAN_INTEREST_RATE

    #loan command -----------------------------------------------------------------
    if message.content.upper ().startswith("E!LOAN"):
        args = message.content.split(" ")
        principal = intify(args[1])
        if len(args) == 1 or len(args) > 2:
            msg = 'To take out a loan, say e!loan `number` to be loaned `number` credits.'
            await client.send_message(message.channel, msg)
        elif principal < 1:
            msg = "You can't choose a principal less than one, silly!"
            await client.send_message(message.channel, msg)
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
                with open('loans.json', 'w') as fp:
                    json.dump(loaninfo, fp, sort_keys = True, indent = 4)
                user_add_value(message.author.id, principal, 'credits')
                msg = 'You were loaned `' + str(principal) + '` credits with a ' + str(LOAN_INTEREST_RATE) + " interest rate (per minute)! You must return it by (hmmmmmmmmmmmmmmmm this is that part we still don't know yet...). (Remember that final amount is calculated using simple interest and that if you don't give it back in time, all of your stats will be reset.)"
                await client.send_message(message.channel, msg)
    
    #checkloan command                                                                                                                                     
    if message.content.upper ().startswith("E!CHECKLOAN"):
        if loans[message.author.id] == False:
            msg = "You don't have a loan to check on!"    
            await client.send_message(message.channel, msg)
        else:
            #something thats shows what the loan is                                                                                                                             
                                                                                                                                         
                                                                                                                                         
    #returnloan command --------------------------------------------------------
    if message.content.upper () == 'E!RETURNLOAN':
        try:
            with open('loans.json', 'r') as fp:
                loan = json.load(fp)
                loaninfo = loan[message.author.id]
                principal = loaninfo['principal']
                time = loaninfo['time']
            time -= (int(datetime.datetime.now().strftime('%d')) * 1440) + int(datetime.datetime.now().strftime('%H') * 60) + int(datetime.datetime.now().strftime('%H')
            loancalnum = int(principal * LOAN_INTEREST_RATE * time)
            if loaninfo[message.author.id] == None
                msg = "You don't have a loan to return!"
                await client.send_message(messsage.channel, msg)
            elif not get_value(message.author.id, 'credits') - loancalnum > 0:
                msg = 'You cannot pay back your loan, as the loan is {} credits and you have '.format(loancalnum) + '{} credits.'.format(get_value(message.author.id, 'credits'))
                await client.send_message(message.channel, msg)
            else:
                loaninfo[message.author.id] = None
                with open('loans.json', 'w') as f:
                    json.dump(loaninfo, f, sort_keys = True, indent = 4)
                user_add_value(message.author.id, principal, 'credits')
                msg = 'You returned your loan for `{}` credits!'.format(loancalnum)
                await client.send_message(message.channel, msg)
        except KeyError:
            msg = "You don't have a loan to return!"
            await client.send_message(messsage.channel, msg)

    #loan command for discord.py rewrite                                                                                                                              
    @commands.group(name = "loan",
                    description = "Loans you credits with interest",
                    aliases = ["l"],
                    brief = "Loans you credits with interest",
                    help = "Loans you however many credits you want for 1% interest per minute.",
                    usage = "e!loan"
                    invoke_without_command = True
                    case_insensitive = True
)
    async def loan(self, ctx, principal: int):
        val = self.get_stats(ctx.author.id, 'credits')
        if principal < 1:
            msg = "You can't choose a principal less than one, silly!"
        else:
                #with statement thing?
                if ctx.author.id in self.REQUESTEDLOAN or self.REQUESTEDLOAN[ctx.author.id]['started']):
                    msg = "You already have a loan, and you can't get two at once! If you want to pay it off, say e!returnloan."
                else:
                    self.REQUESTEDLOAN = {ctx.author.id: {}}
                    self.REQUESTEDLOAN[ctx.author.id]['started'] = True
                    self.REQUESTEDLOAN[ctx.author.id]['principal'] = principal
                    msg = "You asked for a loan of `{}` credits at 1% interest. You now have `{}` credits.".format(pricipal, val)
    await ctx.send(msg)
