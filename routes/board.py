from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

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
        abort(403)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    Board.new(form)
    return redirect(url_for('topic.index'))
