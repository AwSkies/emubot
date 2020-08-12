
    #gives dummy bot the apropriate stats -----------------------------------------
    if message.content.upper ().startswith('E!DUMMYSTATS'):
        if "448272810561896448" in [role.id for role in message.author.roles]:
            args = message.content.split(" ")
            numcredits = args[1:2]
            numemus = args[2:3]
            numdefense = args[3:4]
            user_add_value(559848326904938536, numcredits, 'credits')
            user_add_value(559848326904938536, numemus, 'credits')
            user_add_value(559848326904938536, numdefense, 'credits')
            msg = "Dummy Bot has:"
            msg += "\n:moneybag: `{}` credits.".format(get_value(559848326904938536, 'credits'))
            msg += "\n<:emu:439821394700926976> `{}` emu(s) in storage.".format(get_value(559848326904938536, 'emustorage'))
            msg += "\n:shield: `{}` emu(s) on defense.".format(get_value(559848326904938536, 'emudefense'))
            await client.send_message(message.channel, msg)
        else:
            msg = 'You do not have permission to use this command!'
            await client.send_message(message.channel, msg)

            
    #dummy stats command for rewrite
    @commands.command(name = "dummystats"
                      aliases = ['ds', 'dstats']
                      hidden = True
)
    @commands.has_role('Tester')
    async def adddummystats(self, ctx, numcredits: int, numemus: int, numdefense: int):
        self.add_stats(559848326904938536, numcredits, 'credits')
        self.add_stats(559848326904938536, numemus, 'storage')
        self.add_stats(559848326904938536, numdefense, 'defense')
        msg = "Dummy Bot has:"
        msg += "\n:moneybag: `{}` credits.".format(self.get_stats(559848326904938536, 'credits'))
        msg += "\n<:emu:439821394700926976> `{}` emu(s) in storage.".format(self.get_stats(559848326904938536, 'storage'))
        msg += "\n:shield: `{}` emu(s) on defense.".format(self.get_stats(559848326904938536, 'defense'))
        ctx.send(msg)
