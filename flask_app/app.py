from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

app.secret_key = "a_somewhat_secret_key"

from . import routes