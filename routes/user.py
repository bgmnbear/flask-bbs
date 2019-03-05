from flask import Blueprint, render_template, abort

from models.follow import Follow
from models.reply import Reply
from models.topic import Topic
from models.user import User

from routes import current_user, sort_by_create_time, sort_by_reply_time

main = Blueprint('user', __name__)


@main.route("/<string:username>")
def user(username):
    u = current_user()
    user = User.find_by(username=username)
    if user is not None:
        topic = sort_by_create_time(Topic.find_all(user_id=user.id))
        reply = sort_by_reply_time(Reply.find_all(user_id=user.id))

        topic_id = [r.topic_id for r in reply]
        sorted_topic_id = sorted(set(topic_id), key=topic_id.index)
        sorted_topic = [Topic.find_by(id=id) for id in sorted_topic_id]

        f = Follow.find_by(user_id=user.id)
        following = [User.find_by(id=id) for id in set(f.following_id)]
        follower = [User.find_by(id=id) for id in set(f.follower_id)]

        button_id = "follow"
        if u.id in f.follower_id:
            button_id = "unfollow"

        return render_template("user.html", user=user, ts=topic, ots=sorted_topic, following=following,
                               follower=follower, button_id=button_id)
    else:
        abort(403)


# TODO, did not return a response bug fixes
@main.route("/<string:username>/follow")
def follow(username):
    u = current_user()
    user = User.find_by(username=username)
    if user is not None and u != user:
        u_id = user.id
        Follow.add_follow(u.id, u_id)
    return None


@main.route("/<string:username>/unfollow")
def unfollow(username):
    u = current_user()
    user = User.find_by(username=username)
    if user is not None and u != user:
        u_id = user.id
        Follow.delete_follow(u.id, u_id)
    return None
