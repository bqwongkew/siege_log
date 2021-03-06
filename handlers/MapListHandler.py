
class MapListHandler:
    def __init__(self, maps):
        self.maps = list(map(lambda map_item: map_item.name, maps))

    def can_handle(self, message):
        return message.content.startswith('!maps')

    def get_info(self, message):
        return '!maps to get a list of maps'

    def process(self, message):
        return ", ".join(self.maps)
