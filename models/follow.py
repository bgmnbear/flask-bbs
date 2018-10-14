from models.mongoo import Mongoo


class Follow(Mongoo):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('user_id', int, 0),
            ('following_id', list, []),
            ('follower_id', list, []),
        ]
        return names

    def _get_following_id(self):
        return self.following_id

    def _get_follower_id(self):
        return self.follower_id

    @staticmethod
    def _add_following(user_id, other_id):
        f = Follow.find_by(user_id=user_id)
        f._get_following_id().append(other_id)
        f.save()

    @staticmethod
    def _add_follower(user_id, other_id):
        f = Follow.find_by(user_id=user_id)
        f._get_follower_id().append(other_id)
        f.save()

    @staticmethod
    def _delete_following(user_id, other_id):
        f = Follow.find_by(user_id=user_id)
        f._get_following_id().remove(other_id)
        f.save()

    @staticmethod
    def _delete_follower(user_id, other_id):
        f = Follow.find_by(user_id=user_id)
        f._get_following_id().remove(other_id)
        f.save()

    @staticmethod
    def add_follow(user_id, other_id):
        Follow._add_following(user_id, other_id)
        Follow._add_follower(other_id, user_id)

    @staticmethod
    def delete_follow(user_id, other_id):
        Follow._delete_following(user_id, other_id)
        Follow._delete_follower(other_id, user_id)
