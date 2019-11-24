import discord

from discord.ext import commands
from cogs.UtilsLib import Utils

class Misc(commands.Cog, Utils):
    """Commands that don't really fit into any other category."""
    def __init__(self, bot):
        Utils.__init__(self)
        self.bot = bot

    @commands.command(
        name = "say",
        description = "Makes the bot say whatever you say",
        brief = "Makes the bot say whatever you say",
        help = "Makes the bot says whatever you put after the e!say",
        usage = '[sentence or "sentence"] - makes the bot say [sentence or "sentence"]'
)
    async def say(self, ctx, *args):
        if len(args) == 0:
            msg = "You can't make me send an empty message!"
            await ctx.send(msg)
        else:
            embed = discord.Embed(color = ctx.author.roles[-1].color)
            name = 'The Emu says:'
            embed.add_field(name = name, value = ' '.join(args), inline=False)
            embed.set_footer(text = "-" + str(ctx.author))
            await ctx.message.delete()
            await ctx.send(embed=embed)
        
    @commands.group(
        name = 'guilds',
        description = 'Displays the number of guild the Emu Bot is a part of. Thanks to every one for supporting and using the Emu Bot.',
        brief = 'Guilds the Emu Bot is in',
        aliases = ['guild', 'servers'],
        case_insensitive = True,
        invoke_without_command = True
)
    async def guilds(self, ctx):
        msg = 'The Emu Bot is a part of `{}` guilds. Big thanks to each one for helping out and supporting the Emu Bot.'.format(len(self.bot.guilds))
        await ctx.send(msg)
        
    @guilds.group(
        name = 'list',
        description = 'Lists the names of all the guilds the Emu Bot is a part of.',
        brief = 'Lists guilds the Emu Bot is in',
        alises = ['l']
)
    async def guildlist(self, ctx):
        msg = '__Guilds the Emu Bot is in:\n__'
        for guild in self.bot.guilds:
            msg += '{}\n'.format(guild.name)
        await ctx.send(msg)
    
    @commands.command(
        name = "helpersay",
        aliases = ["hsay", "hs"],
        hidden = True
)
    @commands.has_role('Helpers')
    async def helpersay(self, ctx, *args):
        if len(args) == 0:
            msg = "You can't make me send an empty message!"
        else:
            msg = ' '.join(args)
        await ctx.message.delete()
        await ctx.send(msg)
        
    @commands.group(
        name = "changestatus",
        aliases = ["cs"],
        hidden = True,
        invoke_without_command = True,
        case_insensitive = True
)
    @commands.is_owner()
    async def changestatus(self, ctx, *args):
        if len(args) == 0:
            gamename = "Say e!help"
        else:
            gamename = ' '.join(args)
        game = discord.Game(name = gamename)
        msg = "Status changed to " + gamename
        await self.bot.change_presence(activity = game)
        await ctx.send(msg)
        
    @changestatus.command(
        name = 'clear',
        aliases = ['c', 'r', 'rm', 'remove', 'reset'],
        hidden = True
)
    @commands.is_owner()
    async def reset_status(self, ctx):
        await self.bot.change_presence(activity = None)
        msg = 'Removed playing status'
        await ctx.send(msg)
    
def setup(bot):
    bot.add_cog(Misc(bot))
