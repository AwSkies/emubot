import discord
import json
import os.path

from discord.ext import commands
from cogs.UtilsLib import Utils

class Rewards(commands.Cog, Utils):
    """Ways to view and set (rewards can only be set by server admins) custom rewards that can be bought with credits earned in the Emu Bot game"""
    def __init__(self, bot):
        Utils.__init__(self)
        self.bot = bot
    
    @commands.group(
        name = 'rewards',
        description = 'Lists rewards in this server',
        aliases = ['r', 'rs'],
        brief = 'Lists available rewards',
        help = 'Lists roles available as rewards in this server',
        invoke_without_command = True,
        case_insensitive = True
)
    @commands.guild_only()
    async def rewards(self, ctx):
        with open('rewards.json', 'r') as f:
            rewards = json.load(f)
        try:
            rewards = rewards[str(ctx.message.guild.id)]
            embed = discord.Embed(color = ctx.message.guild.roles[-1].color)
            name = 'Rewards for {}'.format(ctx.guild.name)
            embed.add_field(name = name, value = 'Rewards can be bought with credits earned in the Emu Bot game', inline = False)
            for r in rewards:
                embed.add_field(name = ctx.guild.get_role(r['role']).name,
                                value = 'Description: {} \nCost: {} credit(s)'.format(r['desc'], r['cost']),
                                inline = False)
            await ctx.send(embed=embed)
        except KeyError:
            msg = 'There are no rewards for this server!'
            await ctx.send(msg)

    @rewards.command(
        name = 'add',
        description = 'Register a role as a reward',
        aliases = ['a', 'register', 'r'],
        brief = 'Add a role as a reward (for admins)',
        help = 'Register a role as a reward on your server. Rewards can be bought with credits from the Emu Bot game',
        usage = "[@role mention or role name] [cost] [description]\nRole mention: mention the role (roles to add must be mentionable)\nCost: How many credits the reward costs\nDescription: Write why someone would to have this role. It could be as simple as a color role or give special permissions"
)
    @commands.has_guild_permissions(manage_guild = True)
    @commands.bot_has_guild_permissions(manage_guild = True)
    async def add_rewards(self, ctx, r: str, cost: int, *desc):
        role = ctx.message.role_mentions[0]
        if ctx.message.guild.roles.index(ctx.author.roles[-1]) < ctx.message.guild.roles.index(role):
            msg = "You can't add that role, it's higher than your own"
        else:
            with open('rewards.json', 'r') as f:
                rewards = json.load(f)
            adding_reward = {}
            adding_reward['role'] = int(role.id)
            adding_reward['desc'] = ' '.join(desc)
            adding_reward['cost'] = cost
            try:
                rewards[int(ctx.message.guild.id)].append(adding_reward)
            except KeyError:
                rewards[int(ctx.message.guild.id)] = []
                rewards[int(ctx.message.guild.id)].append(adding_reward)
            with open('rewards.json', 'w') as f:
                json.dump(rewards, f, sort_keys = False, indent = 4)
            msg = 'Ok! Added role "{}" with description "{}" as a reward with the cost of `{}` credits!'.format(role.name, ' '.join(desc), cost)
        await ctx.send(msg)
        
def setup(bot):
    bot.add_cog(Rewards(bot))
