from flask import Blueprint, render_template, redirect, abort

from models.reply import Reply
from models.topic import Topic
from models.user import User
from routes import current_user
from utils import log

main = Blueprint('user', __name__)


@main.route("/<string:username>")
def user(username):
    u = User.find_by(username=username)
    if u is not None:
        ts = Topic.find_all(user_id=u.id)
        ts.reverse()

        t_id = set(i.topic_id for i in Reply.find_all(user_id=u.id))
        ots = list()
        for i in t_id:
            ots.append(Topic.find_by(id=i))
        ots.reverse()
        return render_template("user.html", user=u, ts=ts, ots=ots)
    else:
        abort(404)
