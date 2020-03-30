from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('introdon.config')

db = SQLAlchemy(app)

from introdon.views import views, entries, songs, games, users
