from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app = Flask(__name__, static_folder='../frontend/dist/static', template_folder='../frontend/dist')

cors = CORS(app, supports_credentials=True)

app.config.from_object('introdon.config')

db = SQLAlchemy(app)
ma = Marshmallow(app)

from introdon.views import views, songs, games, users
