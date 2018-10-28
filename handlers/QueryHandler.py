import sqlite3
from TableRenderer import *

class QueryHandler:
    def __init__(self, conn, whitelist):
        self.whitelist = whitelist
        self.conn = conn

    def is_auth(self, user):
        return user.get_full_name() in self.whitelist

    def can_handle(self, message):
        return message.content.startswith('!query')

    def get_info(self, message):
        if (self.is_auth(message.author)):
            return '!query [sql] to run arbitrary sql'
        else:
           return None

    def process(self, message):
        if (not self.is_auth(message.author)):
            return f"{message.author.name} is not authorized"

        sql = message.content[len('!query'):]
        print(f"{message.author.name} is executing {sql}")
        render_sql_table(sql)
