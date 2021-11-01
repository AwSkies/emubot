import argparse
import discord

from discord.ext import commands
from cogs.UtilsLib import Utils

parser = argparse.ArgumentParser(description = 'run the Emu Bot')
parser.add_argument('-d', '--dummy', action = 'store_true', help = 'connect the bot to the dummy account, rather than the main Emu Bot account; used for testing')
args = parser.parse_args()
file = 'bot.token.txt' if not args.dummy else 'dummy.token.txt'

with open(file, 'r') as f:
    TOKEN = f.readline()

with open('promo.txt', 'r') as f:
    PROMO = f.read()
    PROMO = PROMO.strip('\n')

class EmuBot(commands.Bot, Utils):
    def __init__(self):
        DESCRIPTION = '''A discord bot to honor our best friends, the emus. 
With this bot you can use fun (and pointless) commands, earn credits by chatting, use those credits to buy emus, and use those emus to attack or defend against your friends.
This bot was created by CaptainClumsy#3018 with some help from Beastkin#9390
Support the Emu Bot on Patreon: https://patreon.com/emubot
{}'''.format(PROMO)

        self.dummy = args.dummy
        
        commands.Bot.__init__(self,
                             command_prefix = ['e!', 'E!'],
                             description = DESCRIPTION,
                             case_insensitive = True,
                             activity = discord.Game(name = 'Reloading...'))
        Utils.__init__(self, self.dummy)

        self.COGS = ['cogs.fun', 'cogs.game', 'cogs.rewards', 'cogs.misc', 'cogs.helpful', 'cogs.errors', 'cogs.backup', 'cogs.alive']
        if self.dummy:
            self.COGS.remove('cogs.backup')
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
