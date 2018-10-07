from flask import session
from models.user import User


def current_user():
    uid = session.get('user_id', '')
    u = User.find_by(id=uid)
    return u


def sort_by_create_time(topic):
    return sorted(topic, key=lambda topic: topic.create_time, reverse=True)


def sort_by_update_time(topic):
    return sorted(topic, key=lambda topic: topic.update_time, reverse=True)


def sort_by_reply_time(reply):
    return sorted(reply, key=lambda reply: reply.reply_time, reverse=True)


def delete_session():
    session.clear()
