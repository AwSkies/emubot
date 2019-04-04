# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord

TOKEN = 'NDM5NDk4OTc0NDg3OTA0MjU2.DcUs6w.KBOU--o7DtDHLnm87a5MqtRbwSw'

client = discord.Client()

@client.event
async def on_message(message):
    # disallows the bot from replying to itself
    if message.author == client.user:
        return

    if message.content.startswith('e!emu'):
        #msg = 'Emu! {0.author.mention}'.format(message)
        msg = 'https://www.denverzoo.org/sites/default/files/denver_zoo_emu_480x490.jpg'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
