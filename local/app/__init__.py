from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Create a Flask instance
app = Flask(__name__)
app.config.from_object('config')

# Initialize Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .views import views
from .auth import auth

app.register_blueprint(views, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")

from .models import User

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))