from models.mongoo import Mongoo
from models.user import User


class Answer(Mongoo):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('views', int, 0),
            ('title', str, ''),
            ('content', str, ''),
            ('user_id', int, 0),

        ]
        return names

    @classmethod
    def get(cls, id):
        answer = cls.find_by(id=id)
        answer.views += 1
        answer.save()
        return answer

    def replies(self):
        from .reply import Reply
        r = Reply.find_all(answer_id=self.id)
        return r

    def user(self):
        u = User.find(id=self.user_id)
        return u
