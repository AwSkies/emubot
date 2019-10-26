import discord
import threading

from cogs.UtilsLib import Utils
from discord.ext import commands


with open('TOKEN.txt', 'r') as f:
    TOKEN = f.readline()

class EmuBot(commands.Bot, Utils):
    def __init__(self):
        DESCRIPTION = '''A discord bot to honor our best friends, the emus. 
        With this bot you can use fun (and pointless) commands, earn credits by chatting, use those credits to buy emus, and use those emus to attack or defend against your friends.'''
        
        commands.Bot.__init__(self,
                             command_prefix = 'e!',
                             description = DESCRIPTION,
                             case_insensitive = True)
        Utils.__init__(self)
        
        self.COGS = ['cogs.fun', 'cogs.game', 'cogs.misc']
        for cog in self.COGS:
            self.load_extension(cog)
            
    async def on_message(self, message):
        if (not message.author.id in self.SPAMCATCH) or (message.author.id in self.SPAMCATCH and not self.SPAMCATCH[message.author.id]):
            self.add_stats(message.author.id, 10, 'credits')
            self.SPAMCATCH[message.author.id] = True
            def spamtimer():
                self.spamswitch(message.author.id)
            t = threading.Timer(10.0, spamtimer)
            t.start()
            
        await self.process_commands(message)
    
    async def on_command_error(self, ctx, error):
        await ctx.send(str(error))
        print('Message', ctx.message.content, 'caused:')
        print(error)
    
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        await self.change_presence(activity = discord.Game(name = "Say e!help"))
        
if __name__ == '__main__':
    b = EmuBot()
    b.run(TOKEN)
