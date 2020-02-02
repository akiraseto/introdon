from datetime import datetime

from introdon import db


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.Integer, nullable=False)
    button_number = db.Column(db.Integer, nullable=False)
    correct = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, game_id, button_number, correct, result=None):
        self.game_id = game_id
        self.button_number = button_number
        self.correct = correct
        self.result = result
        self.created_at = datetime.now()

    def __repr__(self):
        return '<Entry id:{}>'.format(self.id)
