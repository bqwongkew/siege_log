
from TableRenderer import *

class HelpHandler:
    def __init__(self, handlers):
        self.handlers = handlers

    def can_handle(self, message):
        return message.content.startswith('!help')

    def get_info(self, message):
        return None

    def process(self, message):
        result = 'Valid commands:'

        for handler in self.handlers:
            infoLine = handler.get_info(message)
            if (infoLine is not None):
                result = result + '\n' + infoLine

        return result
