import time

from models.mongoo import Mongoo
from models.user import User


class Question(Mongoo):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('views', int, 0),
            ('title', str, ''),
            ('content', str, ''),
            ('user_id', int, 0),
            ('create_time', int, time.time()),
            ('update_time', int, time.time()),
        ]
        return names

    @classmethod
    def get(cls, id):
        question = cls.find_by(id=id)
        question.views += 1
        question.save()
        return question

    def replies(self):
        from .reply import Reply
        r = Reply.find_all(question_id=self.id)
        return r

    def user(self):
        u = User.find(id=self.user_id)
        return u
