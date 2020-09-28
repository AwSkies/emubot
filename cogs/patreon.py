import discord
import patreon
import json

from discord.ext import commands
from cogs.UtilsLib import Utils
from fuzzywuzzy import process

with open('patreon.token.txt', 'r') as f:
    PTOKEN = f.readline()

class Patreon(commands.Cog, Utils):
    """Patreon commands"""
    def __init__(self, bot):
        Utils.__init__(self, bot.dummy)
        self.bot = bot
        # patreon client initialization and gets ID to fetch 
        self.pclient = patreon.API(PTOKEN)
        self.campaign_id = self.pclient.fetch_campaign().data()[0].id()

    def get_patrons(self):
        '''Gets patrons in shout-out tier'''
        all_pledges = []
        cursor = None
        while True:
            pledges = self.pclient.fetch_page_of_pledges(self.campaign_id, 25, cursor = cursor, fields = {'pledge': ['total_historical_amount_cents', 'declined_since']})
            cursor = self.pclient.extract_cursor(pledges)
            all_pledges += pledges.data()
            if not cursor:
                break
        # gets pledger name and filters out pledges who have been declined and pledges who are not in the shout-out tier, then sorts by amount
        return sorted([{'name': pledge.relationship('patron').attribute('full_name'), 'cents': pledge.attribute('total_historical_amount_cents')} for pledge in all_pledges if (not pledge.attribute('declined_since')) and (pledge.relationship('reward').attribute('amount_cents') >= 1000)], key = lambda pledge : pledge['total_historical_amount_cents'], reverse = True)

    @commands.command(
        name = 'patreon',
        description = 'Support the Emu Bot on Patreon and see current supporters',
        aliases = ['p', 'support'],
        brief = 'Support the Emu Bot on Patreon and see current supporters',
        help = """The Emu Bot runs on the Google Cloud Platform to keep it fast and online all the time. However, this virtual machine is not free, so if you love the Emu Bot and want it to stay fast and working all the time, consider donating.
        Thank you so much to all of the people who support the Emu Bot."""
)
    async def patreon(self, ctx):
        embed = discord.Embed(title = "Patreon", url = "https://patreon.com/emubot", description = "The Emu Bot runs on the Google Cloud platform to keep it fast and online all the time. However, this virtual machine is not free, so if you love the Emu Bot and want it to stay fast and working all the time, consider donating to the Patreon: https://patreon.com/emubot", color=0xf64c04)
        patreon_image = discord.File('pictures/patreon-logo.png', filename = 'patreon-logo.png')
        embed.set_thumbnail(url = 'attachment://patreon-logo.png')
        for patron in self.get_patrons():
            embed.add_field(name = patron['name'], value = 'donated ${}.{}'.format(str(patron['cents'])[:-2], str(patron['cents'])[-2:]))
        await ctx.send(file = patreon_image, embed = embed)

    @commands.command(
        name = 'supporter',
        description = "Use with a Patreon supporter's mame to view their custom message",
        aliases = ['patron'],
        brief = "Patreon supporters' custom messages",
        help = "Use with a Patreon supporter's mame to view their custom message. To see who has a custom message, use `e!patreon` or `e!support`",
        usage = "[supporter's name]"
)
    async def custom_messages(self, ctx, *full_name):
        name = ' '.join(full_name)
        with open('patron_messages.json', 'r') as f:
            patrons = json.load(f)
        if name in [patron['name'] for patron in self.get_patrons()]:
            msg = patrons['message'] if name in patrons.keys() else 'This patron has no custom message yet.'
        else:
            alike_names = process.extract(name, [patron['name'] for patron in self.get_patrons()], limit = 3)
            msg = 'There is no supporter with that name.'
            if len(alike_names) >= 3:
                corrections = [i[0] for i in alike_names]
                msg += '\nDid you mean: `{}` | `{}` | `{}`'.format(*corrections)
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(Patreon(bot))