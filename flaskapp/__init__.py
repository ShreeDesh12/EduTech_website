from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flaskapp.config import Config



db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category= 'info'
bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__, static_folder = "static")
    app.config.from_object(Config)

    from flaskapp.users.routes import users
    from flaskapp.posts.routes import posts
    from flaskapp.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    return app
