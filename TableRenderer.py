import sqlite3

class TableRenderer:
    class Table: 
        def __init__(self):
            self.cols = []
            self.rows = []

    class Column:
        def __init__(self, name):
            self.name = name
            self.width = len(name)

    def __init__(self):
        self.tables = []

    def populate(self, cursor):
        table = self.Table()

        names = list(map(lambda x: x[0], cursor.description))
        for name in names:
            table.cols.append(self.Column(name))

        while True:
            row = cursor.fetchone()
            if row is None:
                break

            rowStrings = []
            for (i, val) in enumerate(row):
                col = table.cols[i]
                rowStrings.append(f"{val}")
                col.width = max(col.width, len(f"{val}"))
            table.rows.append(rowStrings)
        self.tables.append(table)

    def render(self):
        result = "\n```"
        for table in self.tables:
            result += self.renderTable(table) + "\n"
        return result + "```"

    def renderTable(self, table):
        result = ""
        result += self.renderBreak(table) + "\n"
        result += self.renderRow(zip(
            map(lambda col: col.name, table.cols),
            map(lambda col: col.width, table.cols))) + "\n"
        result += self.renderBreak(table) + "\n"

        for row in table.rows:
            result += self.renderRow(zip(row,
                map(lambda col: col.width, table.cols))) + "\n"

        result += self.renderBreak(table) + "\n"
        return result

    def renderBreak(self, table):
        result = "+"
        for col in table.cols:
            result += ("-" * col.width) + "+"
        return result

    def renderRow(self, row):
        result = "|"
        for (val, size) in row:
            result += val.rjust(size, " ") + "|"
        return result

