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
                             case_insensitive = True)
        Utils.__init__(self)
        
        self.COGS = ['cogs.fun', 'cogs.game', 'cogs.misc']
        for cog in self.COGS:
            self.load_extension(cog)
            
    async def on_message(self, message):
        await self.process_commands(message)
    
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            msg = "That command doesn't exist!"
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            msg = "You are not using this command correctly. Use e!help command for information on how to use a a command. The square brackets [] around a word indicate a value you must provide after the command."
        elif isinstance(error, commands.errors.MissingRole):
            msg = "You do not have the required role for this command."
        elif isinstance(error, commands.errors.CommandOnCooldown):
            msg = error
        else:
            msg = error
            print('Message', ctx.message.content, 'caused exception:')
            print(error)
            print(type(error))
        await ctx.send(msg)
        
    
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        await self.change_presence(activity = discord.Game(name = "Say e!help"))
        
if __name__ == '__main__':
    b = EmuBot()
    b.run(TOKEN)
