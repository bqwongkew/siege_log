import sys
import re

from TableRenderer import *

class MapAddNotesHandler:
    def __init__(self, conn, maps):
        self.conn = conn
        self.maps = maps

    def can_handle(self, message):
        return message.content.startswith('!add-note')

    def get_info(self, message):
        return '!add-note [map] [note] to add a note to a map'

    def process(self, message):
        regex_result = re.search('^!add-note (?P<map>\S+) (?P<note>.*)$', message.content)
        if (regex_result is None):
            return "Couldn't parse command arguments"

        map_name = regex_result.group('map')
        note = regex_result.group('note')

        if map_name not in map(lambda x: x.name, self.maps):
            return "{} is not a valid map".format(map_name)

        self.conn.execute("INSERT INTO map_notes (map_name, note) VALUES (?, ?)", [map_name, note])
        (id,) = self.conn.execute('SELECT last_insert_rowid()').fetchone()
        self.conn.commit()

        return "Added note #{} for {}".format(id, map_name)

class MapRemoveNotesHandler:
    def __init__(self, conn, maps):
        self.conn = conn
        self.maps = maps

    def can_handle(self, message):
        return message.content.startswith('!remove-note')

    def get_info(self, message):
        return '!remove-note [id] to remove the note'

    def process(self, message):
        regex_result = re.search('^!remove-note (?P<id>\d+)$', message.content)
        if (regex_result is None):
            return "Couldn't parse command arguments"

        id = int(regex_result.group('id'))

        self.conn.execute("DELETE FROM map_notes WHERE note_id=?", [id])
        self.conn.commit()

        return "Removed note #{}".format(id)

class MapListNotesHandler:
    def __init__(self, conn, maps):
        self.conn = conn
        self.maps = maps

    def can_handle(self, message):
        return message.content.startswith('!notes')

    def get_info(self, message):
        return '!notes [map] to display all saved notes'

    def process(self, message):
        regex_result = re.search('^!notes( (?P<map>\S+))?$', message.content)
        if (regex_result is None):
            return "Couldn't parse command arguments"

        map_name = regex_result.group('map')
        if (map_name is None):
            return render_sql_table(self.conn, "SELECT * FROM map_notes ORDER BY map_name, note_id")

        if map_name not in map(lambda x: x.name, self.maps):
            return "{} is not a valid map".format(map_name)
        
        return render_sql_table(self.conn, "SELECT * FROM map_notes WHERE map_name=? ORDER BY note_id", [map_name])
