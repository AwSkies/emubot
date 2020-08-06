import discord
import json
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
        await self.bot.wait_until_ready()
        if os.path.isfile('users.json'):
            try:
                with open('users.json', 'r') as f:
                    stats = json.load(f)
            except json.decoder.JSONDecodeError:
                msg = 'Corrupted stats file, please replace'
                await self.bot.get_user(369267862050832385).send(msg)
                print(msg)
                return
            
            if os.path.isfile('users.json.bak'):
                os.rename('users.json.bak', 'users.json.bak.bak')
            shutil.copy('users.json', 'users.json.bak')
            if os.path.isfile('users.json.bak.bak'):
                os.remove('users.json.bak.bak')

def setup(bot):
    bot.add_cog(Backup(bot))
