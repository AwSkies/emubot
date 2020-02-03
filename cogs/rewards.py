import discord
import json

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
        aliases = ['reward', 'r', 'rs'],
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
            embed.add_field(name = name, 
                            value = 'Rewards can be bought with credits earned in the Emu Bot game. \nUse e!rewards buy [reward number] to buy a reward, and for moderators, use e!rewards add [@role mention] [cost] [description] to add a role as a reward and use e!rewards remove [reward number] to remove a role as a reward on your server.', 
                            inline = False)
            i = 0
            for r in rewards:
                i += 1
                embed.add_field(name = '{}. {}'.format(i, ctx.guild.get_role(int(r['role'])).name),
                                value = 'Description: {} \nCost: `{}` credit(s)'.format(r['desc'], r['cost']),
                                inline = False)
            await ctx.send(embed=embed)
        except KeyError:
            msg = 'There are no rewards for this server!'
            await ctx.send(msg)

    @rewards.command(
        name = 'add',
        description = 'Register a role as a reward',
        aliases = ['a', 'register', 'reg', 're'],
        brief = 'Add a role as a reward (for admins)',
        help = 'Register a role as a reward on your server, if you have mange server permissions. Rewards can be bought with credits from the Emu Bot game',
        usage = "[@role mention] [cost] [description]\nRole mention: mention the role (roles to add must be mentionable)\nCost: How many credits the reward costs\nDescription: Write why someone would to have this role. It could be as simple as a color role or give special permissions"
)
    @commands.has_guild_permissions(manage_roles = True)
    @commands.bot_has_guild_permissions(manage_roles = True)
    async def add_rewards(self, ctx, r: str, cost: int, *desc):
        role = ctx.message.role_mentions[0]
        with open('rewards.json', 'r') as f:
            rewards = json.load(f)
            if not str(ctx.message.guild.id) in rewards:
                rewards[str(ctx.message.guild.id)] = []
        if ctx.message.guild.roles.index(ctx.author.roles[-1]) < ctx.message.guild.roles.index(role):
            msg = "You can't add that role, it's higher than your own"
        elif role.id in [r['role'] for r in rewards[str(ctx.message.guild.id)]]:
            msg = 'That role is already added as a reward!'
        else:
            adding_reward = {}
            adding_reward['role'] = int(role.id)
            adding_reward['desc'] = ' '.join(desc)
            adding_reward['cost'] = cost
            rewards[str(ctx.message.guild.id)].append(adding_reward)
            with open('rewards.json', 'w') as f:
                json.dump(rewards, f, sort_keys = False, indent = 4)
            msg = 'Ok! Added role "{}" with description "{}" as a reward with the cost of `{}` credits!'.format(role.name, ' '.join(desc), cost)
        await ctx.send(msg)
        
    @rewards.command(
        name = 'remove',
        description = 'Unregister a role as a reward',
        aliases = ['r', 'unregister', 'ur'],
        brief = 'Remove a role as a reward',
        help = 'Remove a role as a reward, if you have manage server permissions',
        usage = '[reward number]'
)
    @commands.has_guild_permissions(manage_roles = True)
    @commands.bot_has_guild_permissions(manage_roles = True)
    async def remove_rewards(self, ctx, r: int):
        with open('rewards.json', 'r') as f:
            rewards = json.load(f)
        try:
            if len(rewards[str(ctx.message.guild.id)]) < r:
                msg = "You're trying to remove a reward that isn't even registered in the first place!"
            else:
                del rewards[str(ctx.message.guild.id)][r - 1]
                with open('rewards.json', 'w') as f:
                    json.dump(rewards, f, sort_keys = False, indent = 4)
                msg = 'Reward removed.'
        except KeyError:
            msg = 'There are no rewards for this server!'
        await ctx.send(msg)
        
    @rewards.command(
        name = 'buy',
        description = 'Buy a role for credits',
        aliases = ['b', 'redeem'],
        brief = 'Buy a role for credits',
        help = 'Buy a registered role shown using the rewards command with credits',
        usage = '[reward number]'
)
    @commands.bot_has_guild_permissions(manage_roles = True)
    async def buy_rewards(self, ctx, r: int):
        with open('rewards.json', 'r') as f:
            rewards = json.load(f)
        try:
            rewards = rewards[str(ctx.message.guild.id)]
            reward = rewards[r - 1]
            role = ctx.message.guild.get_role(int(reward['role']))
            if len(rewards) < r:
                msg = "You're trying to get a reward that isn't even registered in the first place!"
            elif reward['cost'] > self.get_stats(ctx.author.id, 'credits'):
                msg = "You don't have enough credits to buy that role!" 
            elif role in ctx.author.roles:
                msg = 'You already have that role!'
            elif ctx.message.guild.roles.index(ctx.author.roles[-1]) > ctx.message.guild.roles.index(ctx.message.guild.get_member(self.bot.user.id).roles[-1]):
                msg = "I can't edit your roles, as you have a higher role than me. Please contact the moderators of the server and ask them to make my role higher so I can opertate to my full capacity."
            else:
                self.add_stats(ctx.author.id, -reward['cost'], "credits")
                await ctx.author.add_roles(role)
                msg = "You purchased the role {} for {} credits!".format(ctx.message.guild.get_role(int(reward['role'])).name, reward['cost'])
        except KeyError:
            msg = 'There are no rewards for this server!'
        await ctx.send(msg)
        
        @rewards.command(
        name = 'sell',
        description = 'Buy a role for credits',
        aliases = ['s'],
        brief = 'Sell a bought role for credits',
        help = 'Sell a role bought using the rewards command for 3/4 of the credits',
        usage = '[reward number]'
)
    @commands.bot_has_guild_permissions(manage_roles = True)
    async def buy_rewards(self, ctx, r: int):
        with open('rewards.json', 'r') as f:
            rewards = json.load(f)
        try:
            rewards = rewards[str(ctx.message.guild.id)]
            reward = rewards[r - 1]
            role = ctx.message.guild.get_role(int(reward['role']))
            if len(rewards) < r:
                msg = "You're trying to get a reward that isn't even registered in the first place!"
            elif not role in ctx.author.roles:
                msg = "You don't have that role!"
            elif ctx.message.guild.roles.index(ctx.author.roles[-1]) > ctx.message.guild.roles.index(ctx.message.guild.get_member(self.bot.user.id).roles[-1]):
                msg = "I can't edit your roles, as you have a higher role than me. Please contact the moderators of the server and ask them to make my role higher so I can opertate to my full capacity."
            else:
                cost = int(role['cost'] * 0.75)
                self.add_stats(ctx.author.id, -cost, 'credits')
                await ctx.author.remove_roles(role)
                msg = "You sold the role {} for {} credits!".format(ctx.message.guild.get_role(int(reward['role'])).name, cost)
        except KeyError:
            msg = 'There are no rewards for this server!'
        await ctx.send(msg)
    
def setup(bot):
    bot.add_cog(Rewards(bot))
