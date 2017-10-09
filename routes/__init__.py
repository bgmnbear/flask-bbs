from flask import session

from models.user import User


def current_user():
    uid = session.get('user_id', '')
    u = User.find_by(id=uid)
    return u
