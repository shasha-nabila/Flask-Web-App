import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Add Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True   
WTF_CSRF_ENABLED = True

# Secret Key
SECRET_KEY = "featherst0nehaugh"