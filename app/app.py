import flask_login
from flask import Flask

from config import secret_key
from route.login import login

app = Flask(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


def configured_app():
    app = Flask(__name__)
    app.secret_key = secret_key

    app.register_blueprint(login, '/signup')
    app.register_blueprint(login_route, '/signin')

    return app


if __name__ == '__main__':
    config = dict(
        debug=True,
        port=3000,
        threaded=True,
    )
    app = configured_app()
    app.run(**config)
