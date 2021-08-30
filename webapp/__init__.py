from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy(app)
DB_NAME = "webapp.db"

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
app.config["SECRET_KEY"] = "ec9439cfc6c796ae2029594d"

bcrypt = Bcrypt(app)


login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

# def create_database(app):
#     if not path.exists('webapp/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')

from webapp import routes
