import discord
import json

from discord.ext import commands
from discord.ext.commands import errors
from cogs.UtilsLib import Utils
from fuzzywuzzy import process

class ErrorHandler(commands.Cog, Utils):
    def __init__(self, bot):
        Utils.__init__(self)
        self.bot = bot
        self.all_commands = []
        for command in [command for command in self.bot.commands if not command.hidden]:
            name = command.name
            self.all_commands.append(name)
            if isinstance(command, commands.Group):
                names = []
                for subcommand in [subcommand for subcommand in command.commands if not subcommand.hidden]:
                    self.all_commands.append('{} {}'.format(command.name, subcommand.name))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
            
        elif isinstance(error, errors.CheckFailure):
            return
            
        elif isinstance(error, errors.MissingRequiredArgument):
            msg = "You are not using this command correctly. Use e!help command for information on how to use a a command. The square brackets [] around a word indicate a value you must provide after the command."

        elif isinstance(error, errors.MissingRole):
            msg = "You do not have the required role for this command."

        elif isinstance(error, errors.BadArgument):
            msg = "Numbers must be whole numbers and mentions must be mentions. Make sure you aren't giving the wrong type of parameter for a command."

        elif isinstance(error, errors.CommandOnCooldown):
            msg = error
            
        elif isinstance(error, errors.CommandNotFound):
            corrections = []
            for i in process.extract(ctx.message.content.lower().replace('e!', ''), self.all_commands, limit = 3):
                corrections.append(i[0])
            msg = "That command doesn't exist! \nDid you mean: `{}` | `{}` | `{}`".format(*corrections)

        else:
            msg = error
            print('Message', ctx.message.content, 'caused exception:')
            print(error)
            print(type(error))
            print('------')
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
