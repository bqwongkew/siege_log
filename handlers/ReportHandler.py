
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

class ReportHandler:
    def __init__(self, conn, maps):
        self.conn = conn
        self.maps = maps

    def can_handle(self, message):
        return message.content.startswith('!report')

    def get_info(self, message):
        return '!report [map] [result] to add a match'

    def process(self, message):
        items = message.content.split(' ')
        if len(items) != 3:
            return "Please report match in '!report [map] [result]' format"

        (_, map_name, result) = items
        if map_name not in map(lambda x: x.name, self.maps):
            return "{} is not a valid map".format(map_name)

        outcome = next((outcome for outcome in MatchResult.outcomes if outcome.match(result)), None)
        if outcome is None:
            return "{} is not a valid result".format(result)

        report = Report(map_name, outcome.name)
        self.add_report(report)
        return "You {} on {}".format(report.result, report.map)

    def add_report(self, report):
        item = (report.map, report.result)
        self.conn.cursor().execute("INSERT INTO games VALUES(?, ?)", item)
        self.conn.commit()

