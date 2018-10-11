from flask import Flask
from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.board import main as board_routes
from routes.mail import main as mail_routes
from routes.user import main as user_routes
from routes.search import main as search_routes

from config import secret_key


def configured_app():
    app = Flask(__name__)

    app.secret_key = secret_key

    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(mail_routes, url_prefix='/mail')
    app.register_blueprint(user_routes, url_prefix='/user')
    app.register_blueprint(search_routes, url_prefix='/search')

    return app


if __name__ == '__main__':
    config = dict(
        debug=True,
        # host='0.0.0.0',
        port=3000,
        threaded=True,
    )
    app = configured_app()
    app.run(**config)
