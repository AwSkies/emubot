    #give command------------------------------------------
    if message.content.upper ().startswith("E!GIVE"):
        args = message.content.split(" ")
        numcreds = intify(args[1])
        if (len(args) < 2) or (len(args) > 2):
            msg = "Say e!give `number` `@person` to give `@person` `number` credits!"
            await client.send_message(message.channel, msg)
        elif numcreds < 1:
            msg = "You can't give someone less than one credit!"
            await client.send_message(message.channel, msg)
        elif numcreds > get_value(message.author, 'credits':
            msg = "You don't have enough credits for that!"
            await client.send_message(message.channel, msg)
        else:
            uidstr = args[2][2:-1]
            #checks if uid has a !
            if uidstr[0] == '!': 
                uidstr = uidstr[1:]
            if uidstr == client.user.id:
                msg = "You can't give me credits!!!"
                await client.send_message(message.channel, msg)
            elif uidstr == message.author.id:
                msg = "You can't give yourself credits!"
                await client.send_message(message.channel, msg)
            else:
                user_add_value(message.author.id, -numcreds, 'credits')
                user_add_value(uidstr, numcreds, 'credits')
                msg = "{0.author.mention} gave ".format(message) + "<@" + uidstr + "> `{}` credits!".format(str(numcreds))
                await client.send_message(message.channel, msg)
    
    #give command for discord.py rewrite------------------------------------------
    @commands.command(name = "give",
                      description = "Gives credits to another user",
                      aliases = ['g'],
                      brief = "Gives credits to another user",
                      help = "???.",
                      usage = "e!give [number] [@mention]"
                     )

    async def give(self, ctx, numcreds: int, mention: str):
        uid = ctx.message.mentions[0].id
        if not get_stats(ctx.author.id, 'credits') > 0:
            msg = 'You have no credits to give!'
        elif numcreds < 1:
            msg = "You can't give less than one credit!"
        elif numcreds > get_stats(ctx.author.id, 'credits'):
            msg = "You don't have enough credits for that!"
        elif uid == bot.user.id:
            msg = "You can't give me credits!"
        elif uid == ctx.author.id:
            msg = "You can't give yourself credits!"
        else:
            self.add_stats(ctx.message.mention[0].id, numemus, 'credits')
            self.add_stats(ctx.author.id, -numemus, 'credits')
            msg = 'You gave `{}` credits to {1.message.mention[0].mention}.'.format(numcreds, ctx)
        await ctx.send(msg)
