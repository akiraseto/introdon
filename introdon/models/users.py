from datetime import datetime

from flask_login import UserMixin

from introdon import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean)
    sum_game = db.Column(db.Integer)
    sum_answer = db.Column(db.Integer)
    sum_correct = db.Column(db.Integer)
    rate = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, username, password, admin=0, sum_game=0, sum_answer=0, sum_correct=0, rate=0):
        self.username = username
        self.password = password
        self.admin = admin
        self.sum_game = sum_game
        self.sum_answer = sum_answer
        self.sum_correct = sum_correct
        self.rate = rate
        self.created_at = datetime.now()
        self.modified_at = datetime.now()

    def __repr__(self):
        return '<Entry id:{} username:{}>'.format(self.id, self.username)
