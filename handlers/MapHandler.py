
class MapHandler:
    def __init__(self, maps):
        self.maps = maps

    def can_handle(self, message):
        return message.content.startswith('!maps')

    def get_info(self, message):
        return '!maps to get a list of maps'

    def process(self, message):
        return ", ".join(self.maps)
