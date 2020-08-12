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
                loantime = (int(datetime.datetime.now().strftime('%d')) * 1440) + int(datetime.datetime.now().strftime('%H') * 60) + int(datetime.datetime.now().strftime('%H'))
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

    #loan command for discord.py rewrite -------------------------------
    import time
    import math
    from discord.ext import commands, tasks

    LOANINTRATE = 1.10 #per minute
    self.LOAN_CAP = 10000
    self.LOAN_CREDS_PER_HOUR = 500 
    
    @commands.group(
        name = "loan",
        description = "Loans you credits with interest",
        aliases = ["l"],
        brief = "Loans you credits with interest",
        help = "Loans you however many credits you want for {}% interest per minute.".format(int((Utils.LOANINTRATE - 1.0) * 100)),
        usage = "[principal]",
        invoke_without_command = True,
        case_insensitive = True
)
    async def loan(self, ctx, principal: int):
        with open('loans.json', 'r') as f:
            loans = json.load(f)
        if principal < 1:
            msg = "You can't choose a principal less than one, silly!"
        elif principal > self.LOAN_CAP:
            msg = "You can't take out loans greater than `{}` credits!".format(self.LOAN_CAP)
        elif ctx.author.id in loans and loans[ctx.author.id]['active']):
            msg = "You already have a loan, and you can't get two at once! If you want to pay it off, say e!loan return."
        else:
            loans[ctx.author.id] = {}
            loans[ctx.author.id]['active'] = True
            loans[ctx.author.id]['principal'] = principal
            loans[ctx.author.id]['user_id'] = ctx.author.id
            startt = int(time.time())
            t = int((principal / self.LOAN_CREDS_PER_HOUR) * 3600)   #calculate time for one hour, then convert to seconds
            loans[ctx.author.id]['time'] = t + startt           #add calculated time to current time to get time at which loan is due
            with open('loans.json', 'w') as f:
                json.dump(loans, f, sort_keys = True, indent = 4)
            self.add_stats(ctx.author.id, principal, 'credits')
            h = int(math.floor(t / 3600))
            m = int(math.floor((t - (h * 3600)) / 60))
            s = int(math.floor(t - ((h * 3600) + (m * 60))))
            msg = "You were loaned `{}` credits with a {}% interest rate per minute! You must return your loan in `{}` hours `{}` minutes and `{}` seconds. Remember that final amount is calculated using simple interest and if you don't return your loan in time, all of your stats will be reset. You can return your loan at any time with e!returnloan, as long as you have enough money to.".format(principal, int((Utils.LOANINTRATE - 1.0) * 100), d, h, m, s)
        await ctx.send(msg)
        
    @loan.command(
        name = "check",
        description = "Displays info about your loan",
        aliases = ["c"],
        brief = "Displays info about your loan",
        help = "Checks how much time you have on your loan and how much money its for."
)
    async def checkloan(self, ctx):
        with open('loans.json', 'r') as f
            loans = json.load(f)
        if (not ctx.author.id in loans) or (not loans[ctx.author.id]['active']):
            msg = "You don't have a loan to check..."
        else:
            now = int(time.time())
            t = int(loans[ctx.author.id]['time'] - now)
            h = int(math.floor(t / 3600))
            m = int(math.floor((t - (h * 3600)) / 60))
            s = int(math.floor(t - ((h * 3600) + (m * 60))))
            msg = 'You owe `{}` credits with a {}% interest rate per minute. You must return your loan in `{}` hours, `{}` minutes, and `{]` seconds or all your stats will be reset. You can return your loan at any time with `e!loan return`, as long as you have enough money to.'.format(int(loans[ctx.author.id]['principal'] * (Utils.LOANINTRATE / 60) * now), int((Utils.LOANINTRATE - 1.0) * 100), h, m ,s)
        await ctx.send(msg)
        
    @loan.command(
        name = "return",
        description = "Returns the money you owe",
        aliases = ["r"],
        brief = "Returns the money you owe",
        help = "Gives back the money you borrowed for you loan."
)
    async def returnloan(self, ctx):
        with open('loans.json', 'r') as f
            loans = json.load(f)
        if not ctx.author.id in loans or not loans[ctx.author.id]['active']):
            msg = "You don't have a loan to return..."
        elif self.get_value(ctx.author.id, 'credits') < loans[ctx.author.id]['current']:
            msg = "You don't have enough money to pay off your loan!"
        else:
            msg = "You returned `{}` credits to the emu bank. Your loan is finished".format(loans[ctx.author.id]['current'])
            current = loans[ctx.author.id]['current']
            self.add_stats(ctx.author.id, -current, 'credits')
            loans[ctx.author.id]['active'] = False
            loans[ctx.author.id]['principal'] = None
            loans[ctx.author.id]['user_id'] = None
            loans[ctx.author.id]['time'] = None
            with open('loans.json', 'w'):
                json.dump(loans, f, sort_keys = True, indent = 4)
        await ctx.send(msg)
        
    @tasks.loop(seconds = 5)
    async def loan_check(self):
        with open('loans.json', 'r') as f:
            loans = json.load(f)time.time()
        for user_id in loans:
            now = int(time.time())
            loan = loans[user_id]
            if loan['time'] <= now:
                current = int(loan['principal'] * (Utils.LOANINTRATE / 60) * now)
                if self.get_stats(user_id, 'credits') > current:
                    self.add_stats(user_id, -current, 'credits')
                    msg = 'The time to return your loan is over, and the amount, `{}` credits, has automatically been collected from you.'.format(current)
                else:
                    cred = self.get_stats(user_id, 'credits')
                    store = self.get_stats(user_id, 'storage')
                    defse = self.get_stats(user_id, 'defense')
                    self.add_stats(user_id, -cred, 'credits')
                    self.add_stats(user_id, -store, 'storage')
                    self.add_stats(user_id, -defse, 'defense')
                    msg = 'You have not returned your loan in time. All of your stats have been reset.'
                self.bot.get_user(str(user_id)).send(msg)
