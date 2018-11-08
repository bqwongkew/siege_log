# SQL
import sqlite3

# Discord
import discord
from discord import *

# Google Drive
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client as drive_client, tools as drive_tools

# Internal Modules
from MapData import *
from handlers.QueryHandler import *
from handlers.ReportHandler import *
from handlers.MapListHandler import *
from handlers.InfoHandler import *
from handlers.MapNotesHandler import *
from handlers.HelpHandler import *
from handlers.StratHandler import *

# Monkey Patch User's Name + Descriminator
User.get_full_name = lambda self: f"{self.name}#{self.discriminator}"

# Discord connection information
TOKEN = 'NTAxOTAwMTA0MDE0MzY0Njc0.DqgHow.o4UByuQXLn3S6FoSO_y3XxKwy78'
discord_client = discord.Client()

# Connect to SQL Server
conn = sqlite3.connect("test.db")

# Login to Google Drive
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
token_store = file.Storage('token.json')
drive_creds = token_store.get()
if not drive_creds or drive_creds.invalid:
    flow = drive_client.flow_from_clientsecrets('credentials.json', SCOPES)
    drive_creds = drive_tools.run_flow(flow, token_store)
drive_service = build('drive', 'v3', http=drive_creds.authorize(Http()))

# Create message handlers
handlers = [QueryHandler(conn, ["Dazer#7130", "VoidCircuit#2131"]),
           ReportHandler(conn, MapData.maps),
           InfoHandler(conn),
           MapListHandler(MapData.maps),
           MapListNotesHandler(conn, MapData.maps), 
           MapAddNotesHandler(conn, MapData.maps), 
           MapRemoveNotesHandler(conn, MapData.maps),
           StratHandler(drive_service, MapData.maps)]
handlers.append(HelpHandler(handlers))

@discord_client.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == discord_client.user:
        return

    try:
        result = None

        for handler in handlers:
            if handler.can_handle(message):
                result = handler.process(message)
                break;

        if result is None:
            return;

        if (type(result) is discord.Embed):
            await discord_client.send_message(message.channel, embed=result)
        else:
            await discord_client.send_message(message.channel, result)

    except:
        await discord_client.send_message(message.channel, "Encountered exception while processing message")
        raise

@discord_client.event
async def on_ready():
    print('Logged in as')
    print(discord_client.user.name)
    print(discord_client.user.id)
    print('------')

# Start the discord client
discord_client.run(TOKEN)
