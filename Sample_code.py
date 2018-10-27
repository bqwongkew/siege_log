# Work with Python 3.6
import discord
import sqlite3
from TableRenderer import *

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

def getName(user):
    return  f"{user.name}#{user.discriminator}"

queryWhitelist = ["Dazer#7130"]
def process_query(author, content: str):
    if (getName(author) not in queryWhitelist):
        return f"{author.name} is not authorized"

    sql = content[len('!query'):]
    print(f"{author.name} is executing {sql}")

    renderer = TableRenderer()
    renderer.populate(c.execute(sql))
    return renderer.render()

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
    m = "unknown error"
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
        m = 'commands are: \n' \
            '!report [map] [result] to add a match \n' \
            '!maps to get a list of maps \n' \
            '!info to get a list of all results'
        if getName(message.author) in queryWhitelist:
            m = m + ' \n!query [sql] to run arbitrary sql'

    if message.content.startswith('!report'):
        m = process_report(message.content)

    if message.content.startswith('!maps'):
        m = ", ".join(maps)

    if message.content.startswith('!query'):
        m = process_query(message.author, message.content)

    if message.content.startswith('!info'):
        m = ""
        dict = {}
        for row in c.execute("SELECT * FROM games"):
            (map, result) = row
            games = (0, 0, 0) if map not in dict else dict[map]
            # print(f"{map} {map in dict} {games}")
            dict[map] = update_game(result, games)
        for (map, sums) in dict.items():
            (win, loss, draw) = sums
            percent = 100*win/(win+loss) if (win+loss) > 0 else 0
            m += f"{map}: {win} Wins, {loss} Losses. {percent}% \n"

    await client.send_message(message.channel, m)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)