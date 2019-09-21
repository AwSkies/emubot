import discord

TOKEN = 'NTU5ODQ4MzI2OTA0OTM4NTM2.D4ADxQ.pOywPuTo2eWHqVTDsWTnRVDnkeY'

client = discord.Client()

@client.event
async def on_message(message):

    if message.content == 'd!upload':
        await client.send_file(message.channel, '/home/pi/Downloads/binary.png')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
