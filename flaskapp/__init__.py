from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__, static_folder = "static")
app.config['SECRET_KEY'] = '7dchd82hcjjs92nd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECURITY_PASSWORD_SALT'] = "my_website"
#app.config["SQLALchemy_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category= 'info'
bcrypt = Bcrypt(app)

from flaskapp.users.routes import users
from flaskapp.posts.routes import posts
from flaskapp.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
