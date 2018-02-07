from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    flash)

from config import admin
from routes import *

from models.board import Board

main = Blueprint('board', __name__)


@main.route("/admin")
def index():
    u = current_user()
    if u.username == admin['username']:
        return render_template('board/admin_index.html')
    else:
        flash(u'您的当前用户不是管理员！请重新登录')

@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    m = Board.new(form)
    return redirect(url_for('topic.index'))
