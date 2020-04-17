import discord
import os
import shutil

from discord.ext import commands, tasks
from cogs.UtilsLib import Utils

class Backup(commands.Cog, Utils):
    def __init__(self, bot):
        Utils.__init__(self)
        self.bot = bot
        self.backup.start()
        
    def cog_unload(self):
        self.backup.cancel()
        
    @tasks.loop(seconds = 30.0)
    async def backup(self):
        if os.path.isfile('users.json'):
            if os.path.isfile('users.json.bak'):
                os.rename('users.json.bak', 'users.json.bak.bak')
            shutil.copy('users.json', 'users.json.bak')
            if os.path.isfile('users.json.bak.bak'):
                os.remove('users.json.bak.bak')

def setup(bot):
    bot.add_cog(Backup(bot))
