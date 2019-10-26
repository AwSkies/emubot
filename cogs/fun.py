import discord

from discord.ext import commands
from cogs.UtilsLib import Utils

class Fun(commands.Cog, Utils):
    def __init__(self, bot):
        Utils.__init__(self)
        self.bot = bot

    @commands.command(
        name = 'emu',
        description = 'Shows a picture of an emu'
)
    async def emupic(self, ctx):
        await ctx.send(file=discord.File('pictures/emu.jpg'))

    @commands.command(
        name = 'server',
        description = 'Gives a link to the Emu Bot Habitat, the Emu Bot testing and support server'
)
    async def serverlink(self, ctx):
        await ctx.send('Emu Bot Habitat the Emu Bot testing and support server link:\nhttps://discord.gg/2xEQkKs')

    @commands.command(
        name = 'website',
        description = 'Gives a link to the Emu Bot website'
)
    async def websitelink(self, ctx):
        await ctx.send('Emu Bot website link:\nhttps://sites.google.com/view/emu-bot-habitat/home')

    @commands.command(
        name = 'emo',
        description = 'EMO EMU'
)
    async def emopic(self, ctx):
        await ctx.send(file=discord.File('pictures/emo.jpg'))

    @commands.command(
        name = 'history',
        description = 'History of the great war'
)
    async def historyytlink(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=QzYlI-W4sg8')

    @commands.command(
        name = 'wtf',
        description = 'What is even going on here'
)
    async def wtfytlink(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=Ej0ZO79Aqxw8')

    @commands.command(
        name = 'dance',
        description = 'Dance dance revol*emu*'
)
    async def danceytlink(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=2RVZvUJDTUE')

    @commands.command(
        name = 'tapdance',
        description = 'Dance, baby (emu), dance.'
)
    async def tapdanceytlink(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=WW6dtCppZIc')

    @commands.command(
        name = 'godnow',
        description = 'Shows the god emu who is your god now'
)
    async def emusmilepic(self, ctx):
        await ctx.send(file=discord.File('pictures/emu-smile.jpg'))

    @commands.command(
        name = 'news',
        description = ''
)
    async def newspic(self, ctx):
        await ctx.send(file=discord.File('pictures/news.jpg'))

    @commands.command(
        name = 'warstats',
        description = 'Attk, Dfnd, Spec'
)
    async def statspic(self, ctx):
        await ctx.send(file=discord.File('pictures/stats.jpg'))

    @commands.command(
        name = 'godmakesemu',
        description = "What went through god's mind when making an emu"
)
    async def makingemupic(self, ctx):
        await ctx.send(file=discord.File('pictures/making-emu.jpg'))

    @commands.command(
        name = 'screech',
        description = 'Reeeeeeeeeeeeeeeee!'
)
    async def screechpic(self, ctx):
        await ctx.send(file=discord.File('pictures/screech.jpg'))

    @commands.command(
        name = 'realizations',
        description = 'My God, what have I done?'
)
    async def realizepic(self, ctx):
        await ctx.send(file=discord.File('pictures/realize.jpg'))

    @commands.command(
        name = 'veteran',
        description = 'Veteran emu'
)
    async def vetpic(self, ctx):
        await ctx.send(file=discord.File('pictures/veteran.jpg'))

    @commands.command(
        name = 'mle',
        description = '*Major League Emu*'
)
    async def mlepic(self, ctx):
        await ctx.send(file=discord.File('pictures/mle.jpg'))

    @commands.command(
        name = 'onduty',
        description = 'Beware of guard emu'
)
    async def onguardpic(self, ctx):
        await ctx.send(file=discord.File('pictures/on-guard.png'))

    @commands.command(
        name = 'grumpy',
        description = 'Grumpy emu'
)
    async def grumpypic(self, ctx):
        await ctx.send(file=discord.File('pictures/grumpy.png'))

    @commands.command(
        name = 'smoile',
        description = 'Smoily emu'
)
    async def smoilepic(self, ctx):
        await ctx.send(file=discord.File('pictures/smoile.png'))

    @commands.command(
        name = 'shark',
        description = '"Humans are friends, not food"'
)
    async def sharkpic(self, ctx):
        await ctx.send(file=discord.File('pictures/shark.png'))

    @commands.command(
        name = 'vampire',
        description = "So what if he's an emu, he still vons to zuck your blud"
)
    async def vampirepic(self, ctx):
        await ctx.send(file=discord.File('pictures/vampire.png'))

    @commands.command(
        name = 'upsidedown',
        description = 'umE'
)
    async def upsidedownpic(self, ctx):
        await ctx.send(file=discord.File('pictures/umE.png'))

    @commands.command(
        name = 'aaa',
        description = 'Dun dun duuuuuuuuuuuun'
)
    async def aaapic(self, ctx):
        await ctx.send(file=discord.File('pictures/aaa.png'))

    @commands.command(
        name = 'xing',
        description = 'Watch out for emus'
)
    async def xingpic(self, ctx):
        await ctx.send(file=discord.File('pictures/xing.jpg'))

    @commands.command(
        name = 'scout',
        description = 'An emu scouting the territory that will soon be his'
)
    async def scoutarticlelink(self, ctx):
        await ctx.send('http://www.abc.net.au/news/2016-10-22/emu-found-wandering-along-arizona-highway/7957198')

    @commands.command(
        name = 'war',
        description = 'Information about the great war'
)
    async def warwikilink(self, ctx):
        await ctx.send('https://en.wikipedia.org/wiki/Emu_War')

def setup(bot):
    bot.add_cog(Fun(bot))
