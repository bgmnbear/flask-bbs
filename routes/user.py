from flask import Blueprint, render_template, redirect, abort

from models.follow import Follow
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

        f = Follow.find_by(user_id=u.id)

        following = [User.find_by(id=id)for id in f.following_id]
        follower = [User.find_by(id=id)for id in f.follower_id]
        print('following', following)

        return render_template("user.html", user=u, ts=ts, ots=ots, following=following, follower=follower)
    else:
        abort(404)


# TODO, did not return a response bug fixes
@main.route("/<string:username>/follow")
def follow(username):
    c_u = current_user()
    u = User.find_by(username=username)
    log('finish')
    if u is not None:
        u_id = u.id
        Follow.add_follow(c_u.id, u_id)
    return None
