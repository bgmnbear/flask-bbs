from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    send_from_directory,
)

from models.user import User
import os
import uuid

from routes import delete_session
from utils import log

main = Blueprint('index', __name__)


def current_user():
    user_id = session.get('user_id', -1)
    u = User.find_by(id=user_id)
    return u


# TODO, debug mode
@main.route("/")
def index():
    # Just for debug and test
    delete_session()

    u = current_user()
    return render_template("index.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('topic.index'))
    else:
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/setting')
def setting():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('setting.html', user=u)


@main.route('/setting/', methods=['POST'])
def change_password():
    form = request.form
    User.change_password(form)
    return redirect(url_for('.index'))


def valid_suffix(suffix):
    valid_type = ['jpg', 'png', 'jpeg']
    return suffix in valid_type


@main.route('/image/add', methods=["POST"])
def add_img():
    u = current_user()
    file = request.files['avatar']
    suffix = file.filename.split('.')[-1]
    if valid_suffix(suffix):
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        # TODO, get path dynamically
        file.save(os.path.join('E:\\flask-bbs\\user_image', filename))

        u.user_image = '/uploads/' + filename
        u.save()

    return redirect(url_for(".setting"))


@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory('user_image', filename)
