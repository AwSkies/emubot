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
        
        # create json file for rewards if it doesn't exist yet
        if not os.path.isfile('rewards.json'):
            with open('rewards.json', 'w'):
                json.dump({}, f, sort_keys = True, indent = 4)
    
    @commands.group(
        name = 'rewards',
        description = 'Lists rewards in this server',
        aliases = ['r', 'rs'],
        brief = 'Lists available rewards',
        help = 'Lists roles available as rewards in this server'
)
    @commands.guild_only()
    async def rewards(self, ctx):
        with open('rewards.json', 'r') as f:
            rewards = json.load(f)
            rewards = rewards[int(ctx.message.guild.id)]
        embed = discord.Embed(color = ctx.message.guild.roles[-1].color)
        name = 'Rewards for {}'.format(ctx.guild.name)
        embed.add_field(name = name, value = 'Rewards can be bought with credits earned in the Emu Bot game', inline = False)
        for r in rewards:
            embed.add_field(name = r['role'].name,
                            value = 'Description: {} Cost: {} credits\n'.format(r['desc'].name, r['cost']),
                            inline = False)
        await ctx.send(embed=embed)

    @rewards.command(
        name = 'add',
        description = 'Register a role as a reward',
        aliases = ['a', 'register', 'add'],
        brief = 'Add a role as a reward',
        help = 'Register a role as a reward on your server. Rewards can be bought with credits from the Emu Bot game',
        usage = "[@role mention or role name] [cost] [description]\nRole mention: mention the role (roles to add must be mentionable)\nCost: How many credits the reward costs\nDescription: Write why someone would to have this role. It could be as simple as a color role or give special permissions"
)
    @commands.has_guild_permissions(manage_server = True)
    @commands.bot_has_guild_permissions(manage_server = True)
    async def add_rewards(self, ctx, r: str, cost: int, *desc):
        role = ctx.message.mentions[0]
        if ctx.message.guild.index(ctx.author.roles[-1]) < ctx.message.guild.roles.index(role):
            msg = "You can't add that role, it's higher than your own"
        else:
            with open('rewards.json', 'r') as f:
                rewards = json.load(f)
            adding_reward = {}
            adding_reward['role'] = role
            adding_reward['desc'] = ' '.join(desc)
            adding_reward['cost'] = cost
            try:
                rewards[int(ctx.message.guild.id)].append(adding_reward)
            except KeyError:
                rewards[int(ctx.message.guild.id)] = []
                rewards[int(ctx.message.guild.id)].append(adding_reward)
            with open('rewards.json', 'r') as f:
                json.dump(rewards, f, sort_keys = True, indent = 4)
            msg = 'Ok! Added role "{}" with description "{}" as a reward with the cost of `{}` credits!'.format(role.name, ' '.join(desc), cost)
        await ctx.send(msg)
        
def setup(bot):
    bot.add_cog(Rewards(bot))
