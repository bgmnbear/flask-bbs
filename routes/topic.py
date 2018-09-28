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


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ts = Topic.all()
    else:
        ts = Topic.find_all(board_id=board_id)
    ts = sort_by_ut(ts)
    token = str(uuid.uuid4())
    u = current_user()
    if u is None:
        abort(403)
    else:
        csrf_tokens['token'] = u.id
        bs = Board.all()
        return render_template("topic/index.html",
                               user=u,
                               ms=ts,
                               token=token,
                               bs=bs,
                               bid=board_id,
                               bbs_time=bbs_time)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    u_id = m.user_id
    u = User.find_by(id=u_id)
    b = m.board()
    ct = m.create_time
    ut = m.update_time
    return render_template("topic/detail.html",
                           topic=m,
                           user=u,
                           board=b,
                           create_time=ct,
                           update_time=ut,
                           bbs_time=bbs_time)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/delete")
def delete():
    id = int(request.args.get('id'))
    # token = request.args.get('token')
    u = current_user()
    # if token in csrf_tokens and csrf_tokens[token] == u.id:
    #     csrf_tokens.pop(token)
    if u is not None and u.username == config.admin['username']:
        Topic.delete(id)
        return redirect(url_for('.index'))
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
    # log('new_csrf_token', token)
    bs = Board.all()
    return render_template("topic/new.html", bs=bs, token=token, bid=board_id)
