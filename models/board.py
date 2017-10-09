import time
from models.mongoo import Mongoo


class Board(Mongoo):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('title', str, ''),
        ]
        return names
