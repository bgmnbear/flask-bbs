from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from routes import *

from models.topic import Topic
from models.board import Board

from utils import date_time, date, log, bbs_time

import uuid
import config

main = Blueprint('topic', __name__)

csrf_tokens = dict()


# TODO, refactor
@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        topic = Topic.all()
    else:
        topic = Topic.find_all(board_id=board_id)
    topic = sort_by_update_time(topic)
    token = str(uuid.uuid4())
    u = current_user()
    if u is None:
        abort(403)
    else:
        csrf_tokens['token'] = u.id
        board = Board.all()
        return render_template("topic/index.html",
                               user=u,
                               ms=topic,
                               token=token,
                               bs=board,
                               bid=board_id,
                               bbs_time=bbs_time)


@main.route('/<int:id>')
def detail(id):
    topic = Topic.get(id)
    user_id = topic.user_id
    user = User.find_by(id=user_id)
    board = topic.board()
    create_time = topic.create_time
    update_time = topic.update_time
    return render_template("topic/detail.html",
                           topic=topic,
                           user=user,
                           board=board,
                           create_time=create_time,
                           update_time=update_time,
                           bbs_time=bbs_time)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    topic = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=topic.id))


@main.route("/delete")
def delete():
    id = int(request.args.get('id'))
    u = current_user()
    if u is not None and u.username == config.admin['username']:
        Topic.delete(id)
        return redirect(url_for('.index'))
    else:
        abort(403)


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    csrf_tokens[token] = u.id
    return token


@main.route("/new")
def new():
    board_id = int(request.args.get('board_id'))
    token = new_csrf_token()
    board = Board.all()
    return render_template("topic/new.html", bs=board, token=token, bid=board_id)
