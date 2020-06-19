from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('introdon.config_flask')

db = SQLAlchemy(app)
ma = Marshmallow(app)

from introdon.views import views, songs, games, users
