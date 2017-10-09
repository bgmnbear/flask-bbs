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
from utils import date_time, date, log

main = Blueprint('topic', __name__)

import uuid

csrf_tokens = dict()


@main.route("/")
def index():
    # board_id = 2
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.find_all(board_id=board_id)
    token = str(uuid.uuid4())
    u = current_user()
    csrf_tokens['token'] = u.id
    bs = Board.all()
    return render_template("topic/index.html", user=u, ms=ms, token=token, bs=bs, bid=board_id)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    u_id = m.user_id
    u = User.find_by(id=u_id)
    b = m.board()
    ct = date(m.create_time)
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m, user=u, board=b, create_time=ct)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/delete")
def delete():
    id = int(request.args.get('id'))
    token = request.args.get('token')
    u = current_user()
    # 判断 token 是否是我们给的
    if token in csrf_tokens and csrf_tokens[token] == u.id:
        csrf_tokens.pop(token)
        if u is not None:
            print('删除 topic 用户是', u, id)
            Topic.delete(id)
            return redirect(url_for('.index'))
        else:
            abort(404)
    else:
        abort(403)


def new_csrf_token():
    u = current_user()
    log('user', u)
    token = str(uuid.uuid4())
    csrf_tokens[token] = u.id
    return token


@main.route("/new")
def new():
    board_id = int(request.args.get('board_id'))
    token = new_csrf_token()
    bs = Board.all()
    return render_template("topic/new.html", bs=bs, token=token, bid=board_id)
