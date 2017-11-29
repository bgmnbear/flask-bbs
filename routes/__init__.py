from flask import session

from models.user import User


def current_user():
    uid = session.get('user_id', '')
    u = User.find_by(id=uid)
    return u


def sort_by_ct(topics):
    return sorted(topics, key=lambda topic: topic.create_time, reverse=True)


def sort_by_ut(topics):
    return sorted(topics, key=lambda topic: topic.update_time, reverse=True)


def sort_by_rt(replys):
    return sorted(replys, key=lambda reply: reply.reply_time, reverse=True)


def delete_session():
    session.clear()