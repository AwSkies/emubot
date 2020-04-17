import discord

from discord.ext import commands
from cogs.UtilsLib import Utils

with open('TOKEN.txt', 'r') as f:
    TOKEN = f.readline()

class EmuBot(commands.Bot, Utils):
    def __init__(self):
        DESCRIPTION = '''A discord bot to honor our best friends, the emus. 
        With this bot you can use fun (and pointless) commands, earn credits by chatting, use those credits to buy emus, and use those emus to attack or defend against your friends.
        This bot was created by CaptainClumsy#3018 with some help from @Beastkin#9390'''
        
        commands.Bot.__init__(self,
                             command_prefix = ['e!', 'E!'],
                             description = DESCRIPTION,
                             case_insensitive = True,
                             activity = discord.Game(name = 'Reloading...'))
        Utils.__init__(self)
        
        self.COGS = ['cogs.fun', 'cogs.game', 'cogs.rewards', 'cogs.misc', 'cogs.helpful', 'cogs.errors', 'cogs.backup']
        for cog in self.COGS:
            self.load_extension(cog)
            
    async def on_message(self, message):
        await self.process_commands(message)
    
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        await self.change_presence(activity = discord.Game(name = 'Say e!help'))
        
if __name__ == '__main__':
    b = EmuBot()
    b.run(TOKEN)
