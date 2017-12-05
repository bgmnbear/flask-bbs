from flask import Blueprint, render_template, redirect, abort, request

from models.reply import Reply
from models.topic import Topic
from models.user import User
from routes import current_user, sort_by_ct, sort_by_ut, sort_by_rt
from utils import log

main = Blueprint('search', __name__)

@main.route('')
def search():
    q = request.args.get('q')
    ts = Topic.find_all(title=q)
    us = User.find_by(username=q)
    return render_template('search.html', ts=ts, us=us)
