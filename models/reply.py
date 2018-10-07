import time
from models.mongoo import Mongoo


class Reply(Mongoo):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('content', str, ''),
            ('topic_id', int, 0),
            ('user_id', int, 0),
            ('reply_time', int, time.time()),
        ]
        return names

    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u
