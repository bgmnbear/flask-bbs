import time
from models.mongoo import Mongoo
from models.user import User


class Topic(Mongoo):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('views', int, 0),
            ('title', str, ''),
            ('content', str, ''),
            ('user_id', int, 0),
            ('board_id', int, 0),
            ('create_time', int, time.time()),
            ('update_time', int, time.time()),
        ]
        return names

    @classmethod
    def get(cls, id):
        topic = cls.find_by(id=id)
        topic.views += 1
        topic.save()
        return topic

    def replies(self):
        from .reply import Reply
        r = Reply.find_all(topic_id=self.id)
        return r

    def board(self):
        from .board import Board
        b = Board.find(self.board_id)
        return b

    def user(self):
        u = User.find(id=self.user_id)
        return u
