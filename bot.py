import discord

from cogs.UtilsLib import Utils
from discord.ext import commands

with open('TOKEN.txt', 'r') as f:
    TOKEN = f.readline()

class EmuBot(commands.Bot, Utils):
    def __init__(self):
        DESCRIPTION = '''A discord bot to honor our best friends, the emus. 
        With this bot you can use fun (and pointless) commands, earn credits by chatting, use those credits to buy emus, and use those emus to attack or defend against your friends.'''
        
        commands.Bot.__init__(self,
                             command_prefix = ['e!', 'E!'],
                             description = DESCRIPTION,
                             case_insensitive = True,
                             activity = discord.Game(name = 'Say e!help'))
        Utils.__init__(self)
        
        self.COGS = ['cogs.fun', 'cogs.game', 'cogs.misc', 'cogs.helpful', 'cogs.errors']
        for cog in self.COGS:
            self.load_extension(cog)
            
    async def on_message(self, message):
        await self.process_commands(message)
    
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        
if __name__ == '__main__':
    b = EmuBot()
    b.run(TOKEN)
