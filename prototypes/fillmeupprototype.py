        #fill testers to a 20,000 credits, 15 emus in storage, and 5 emus on defense
    if message.content.upper ().startswith('E!FILLMEUP'):
        if "448272810561896448" in [role.id for role in message.author.roles]:
            #sets credits to zero
            user_add_value(message.author.id, -get_value(message.author.id, 'credits'), 'credits')
            user_add_value(message.author.id, -get_value(message.author.id, 'emustorage'), 'emustorage')
            user_add_value(message.author.id, -get_value(message.author.id, 'emudefense'), 'emudefense')
            #adds amount of credits
            user_add_value(message.author.id, 20000, 'credits')
            user_add_value(message.author.id, maxemus - maxdefense, 'emustorage')
            user_add_value(message.author.id, maxdefense, 'emudefense')
            msg = 'You are topped off, tester!'
            await client.send_message(message.channel, msg)
        else:
            msg = 'You do not have permission to use this command!"
            await client.send_message(message.channel, msg)

#fillmeup command rewrite
    @commands.command(name = "fillmeup",
                      description = "Gives credits to another user",
                      aliases = ['fill', 'fmu'],
                      brief = "Gives credits to another user",
                      help = "???.",
                      usage = "e!give [number] [@mention]",
                      hidden = True
)
    async def give(self, ctx):
        if "448272810561896448" in [role.id for role in message.author.roles]: #or something
            self.add_stats(ctx.author.id, -(), 'credits')
            self.add_stats(ctx.author.id, -(), 'storage')
            self.add_stats(ctx.author.id, -(), 'defense')
            self.add_stats(ctx.author.id, 20000, 'credits')
            self.add_stats(ctx.author.id, (self.MAXEMUS - self.get_stats(ctx.author.id, 'defense')), 'storage')
            self.add_stats(ctx.author.id, (self.MAXEMUS - self.get_stats(ctx.author.id, 'storage')), 'defense')
            msg = 'You are topped off, tester!'
        else:
            msg = 'You do not have permission to use this command!'
        ctx.send(msg)
