from flask import Blueprint, render_template, redirect, abort, request
from models.topic import Topic
from models.user import User
from routes import sort_by_create_time

main = Blueprint('search', __name__)


@main.route('')
def search():
    q = request.args.get('q')
    ts = sort_by_create_time(Topic.search(q))
    u = User.find_by(username=q)
    return render_template('search.html', ts=ts, u=u)
