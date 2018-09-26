from models.mongoo import Mongoo


class Follow(Mongoo):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('user_id', int, 0),
            ('follower_id', list, 0),
            ('following_id', list, 0),
        ]
        return names

    def get_follower(self):
        pass

    def get_following(self):
        pass

    def add_follower(self):
        pass