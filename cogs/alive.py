import discord

from discord.ext import commands
from flask import Flask
from threading import Thread
from cogs.UtilsLib import Utils

class Alive(commands.Cog, Utils):
    """Keeps the bot's webserver alive keeping the replit instance from stopping"""

    app = Flask(' ')

    def __init__(self, bot):
        Utils.__init__(self, bot.dummy)
        self.bot = bot

        self.app = Flask(' ')
        self.keep_alive()

    @app.route('/')
    def main(self):
        return "Living"

    def run(self):
        self.app.run(host = "0.0.0.0", port = 8080)

    def keep_alive(self):
        server = Thread(target = self.run)
        server.start()

def setup(bot):
    bot.add_cog(Alive(bot))
