from functools import reduce

import sys
import re

import discord
import calendar
import time

ROOT_FOLDER_ID = '1zXfFoSqgUmddHl5gk3r6Zr4zUsoYN-kL'

class StratHandler:
    def __init__(self, service, maps):
        self.service = service
        self.maps = maps

    def can_handle(self, message):
        return message.content.startswith('!strats')

    def get_info(self, message):
        return '!strat [search terms] to search for strats and display them'

    def process(self, message):
        regex_result = re.search('^!strats( -map (?P<map>\S+))?( -side (?P<side>attack|defense+))?( -site (?P<site>\S+))?( -num (?P<num>\d+))?', message.content)
        if (regex_result is None):
            return "Couldn't parse command arguments"
        
        map_name = regex_result.group('map')
        side = regex_result.group('side')
        site = regex_result.group('site')
        num = regex_result.group('num')

        if (map is not None) and (map_name not in map(lambda x: x.name, self.maps)):
            return "{} is not a valid map".format(map_name)

        files = list(filter(lambda x: \
            (map_name is None or map_name.lower() == x['map']) and \
            (side is None or side.lower() == x['side']) and \
            (site is None or site.lower() in x['site']) and \
            (num is None or int(num) == x['num']), self.get_all_files()))

        if (len(files) == 0):
            return "Found no files"

        if (len(files) == 1):
            file = files[0]
            embed = discord.Embed(title="Found: {} - {}".format(file['map'], file['name']),
                                description="{}".format(file['docUrl']),
                                color=0xffffff)
            embed.set_image(url=file['imageUrl'])
            return embed

        file_names = map(lambda x: " - {}".format(x['name']), files)
        return '```' + reduce(lambda lhs, rhs: "{}\n{}".format(lhs, rhs), file_names) + '```'

    def get_all_files(self):
        all_files = []
        folders = self.query_folder(self.service, ROOT_FOLDER_ID)
        for folder in folders:
            if (folder['name'].startswith('z_')):
                continue;
            files = self.query_folder(self.service, folder['id'])
            print(files)
            for file in files:
                all_files.append({
                    'map': folder['name'].lower(),
                    'side': 'attack'.lower(),
                    'site': file['name'].lower(),
                    'num': 0,
                    'name': file['name'],
                    'id': file['id'],
                    'docUrl': "https://docs.google.com/drawings/d/{}/edit".format(file['id']),
                    'imageUrl': "https://docs.google.com/drawings/u/0/d/{}/export/jpeg?timestamp={}".format(file['id'], calendar.timegm(time.gmtime()))
                })
        return all_files

    def query_folder(self, service, id):
        folderQuery = "'{}' in parents".format(id)
        fieldQuery = "files(id, name)"
        return service.files() \
            .list(q=folderQuery, fields=fieldQuery) \
            .execute()['files']
