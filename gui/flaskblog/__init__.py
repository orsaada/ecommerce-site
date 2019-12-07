import os
from flask import Flask
# from flask_bcrypt import Bcrypt
from src.set import Setting

app = Flask(__name__)
# secret key for session management
app.secret_key = os.urandom(24)
Setting.startup()
# bcrypt = Bcrypt(app)

from gui.flaskblog import routes
