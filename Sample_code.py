# Work with Python 3.6
import sqlite3
import discord
from discord import *
from handlers.QueryHandler import *
from handlers.MapHandler import *
from handlers.InfoHandler import *

User.get_full_name = lambda self: f"{self.name}#{self.discriminator}"

conn = sqlite3.connect("test.db")
c = conn.cursor()

class Report:
    def __init__(self, map_name, result):
        self.map = map_name
        self.result = result

    def get_report(self):
        return "{} on {}".format(self.result, self.map)


class MatchResult:
    def __init__(self, name, *names):
        self.name = name
        self.list = list(names)
        self.list.append(name)

    def match(self, result):
        return result.lower() in self.list

MatchResult.win = MatchResult("won", "win", "victory")
MatchResult.lose = MatchResult("lost", "lose", "loss", "defeat")
MatchResult.draw = MatchResult("drew", "draw")
MatchResult.outcomes = [MatchResult.win, MatchResult.lose, MatchResult.draw]

maps = ["bank", "border", "chalet", "club", "coastline", "consulate", "hereford", "kafe", "oregon",
        "skyscraper", "theme park"]
results = ["win", "loss", "draw"]

handlers = [QueryHandler(conn, ["Dazer#7130"]), InfoHandler(conn), MapHandler(maps)]

def process_report(content):
    items = content.split(' ')
    if len(items) != 3:
        return "please report match in '!report [map] [result]' format"
    (_, map_name, result) = items
    if map_name not in maps:
        return "{} is not a valid map".format(map_name)
    outcome = next((outcome for outcome in MatchResult.outcomes if outcome.match(result)), None)
    if outcome is None:
        return "{} is not a valid result".format(outcome)

    report = Report(map_name, outcome.name)
    add_report(report)
    return "You {} on {}".format(report.result, report.map)

def add_report(report):
    item = (report.map, report.result)
    c.execute("INSERT INTO games VALUES(?, ?)", item)
    conn.commit()

def update_game(result, sum):
    (win, loss, draw) = sum
    if result == "won":
        win += 1
    elif result == "lost":
        loss += 1
    elif result == "draw":
        draw += 1
    return win, loss, draw


TOKEN = 'NTAxOTAwMTA0MDE0MzY0Njc0.DqgHow.o4UByuQXLn3S6FoSO_y3XxKwy78'

client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    try:
        result = "Couldn't process message"
        if message.content.startswith('!help'):
            result = 'commands are: \n' \
                '!report [map] [result] to add a match'\

            for handler in handlers:
                infoLine = handler.get_info(message)
                if (infoLine is not None):
                    result = result + '\n' + infoLine

        if message.content.startswith('!report'):
            result = process_report(message.content)

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


client.run(TOKEN)