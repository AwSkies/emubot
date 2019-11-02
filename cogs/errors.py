import discord

from discord.ext import commands
from discord.ext.commands import errors
from cogs.UtilsLib import Utils

class ErrorHandler(commands.Cog, Utils):
    def __init__(self, bot):
        Utils.__init__(self)
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
            
        elif isinstance(error, errors.CommandNotFound):
            msg = "That command doesn't exist!"
            
        elif isinstance(error, errors.MissingRequiredArgument):
            msg = "You are not using this command correctly. Use e!help command for information on how to use a a command. The square brackets [] around a word indicate a value you must provide after the command."

        elif isinstance(error, errors.MissingRole):
            msg = "You do not have the required role for this command."

        elif isinstance(error, errors.BadArgument):
            msg = "Numbers must be whole numbers and mentions must be mentions. Make sure you aren't giving the wrong type of parameter for a command."

        elif isinstance(error, errors.CommandOnCooldown):
            msg = error

        else:
            msg = error
            print('Message', ctx.message.content, 'caused exception:')
            print(error)
            print(type(error))
            print('------')
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
