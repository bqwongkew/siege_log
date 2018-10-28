# Work with Python 3.6
import sqlite3
import discord
from discord import *
from MapData import *

from handlers.QueryHandler import *
from handlers.ReportHandler import *
from handlers.MapHandler import *
from handlers.InfoHandler import *
from handlers.HelpHandler import *

# Monkey Patch User's Name + Descriminator
User.get_full_name = lambda self: f"{self.name}#{self.discriminator}"

# Discord connection information
TOKEN = 'NTAxOTAwMTA0MDE0MzY0Njc0.DqgHow.o4UByuQXLn3S6FoSO_y3XxKwy78'
client = discord.Client()

# Connect to SQL Server
conn = sqlite3.connect("test.db")

# Create message handlers
handlers = [QueryHandler(conn, ["Dazer#7130", "VoidCircuit#2131"]),
            ReportHandler(conn, MapData.maps), InfoHandler(conn), MapHandler(MapData.maps)]
handlers.append(HelpHandler(handlers))

@client.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == client.user:
        return

    try:
        result = "Couldn't process message"

        for handler in handlers:
            if handler.can_handle(message):
                result = handler.process(message)
                break;

        await client.send_message(message.channel, result)

    except:
        await client.send_message(message.channel, "Encountered exception while processing message")
        raise

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# Start the discord client
client.run(TOKEN)
