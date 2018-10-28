
from TableRenderer import *

class InfoHandler:
    def __init__(self, conn):
        self.conn = conn

    def can_handle(self, message):
        return message.content.startswith('!info')

    def get_info(self, message):
        return '!info to get a list of all map results'

    def process(self, message):
        sql = '''
        SELECT
            map AS Map,
            SUM(result='won') AS Wins,
            SUM(result='lost') AS Losses
        FROM games
        GROUP BY map'''

        return render_sql_table(self.conn, sql)
