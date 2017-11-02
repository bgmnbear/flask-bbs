from flask import Blueprint, render_template, redirect, abort

from models.reply import Reply
from models.topic import Topic
from models.user import User
from routes import current_user, sort_by_ct, sort_by_ut, sort_by_rt
from utils import log

main = Blueprint('user', __name__)


@main.route("/<string:username>")
def user(username):
    u = User.find_by(username=username)
    if u is not None:
        ts = sort_by_ct(Topic.find_all(user_id=u.id))
        rs = sort_by_rt(Reply.find_all(user_id=u.id))
        ots_ids = [r.topic_id for r in rs]
        ots_id = sorted(set(ots_ids), key=ots_ids.index)
        ots = [Topic.find_by(id=i) for i in ots_id]
        return render_template("user.html", user=u, ts=ts, ots=ots)
    else:
        abort(404)
