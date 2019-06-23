from flask import Flask

app = Flask(__name__)

app.secret_key = "a_somewhat_secret_key"

from . import routes