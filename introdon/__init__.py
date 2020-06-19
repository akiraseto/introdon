from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('introdon.config_flask')

db = SQLAlchemy(app)
ma = Marshmallow(app)

# DEVツール:DEBUG=TRUEにしないと使えない
toolbar = DebugToolbarExtension(app)

from introdon.views import views, songs, games, users
