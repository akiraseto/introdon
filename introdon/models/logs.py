from datetime import datetime

from introdon import db


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.Integer, nullable=False)
    question_num = db.Column(db.Integer, nullable=False)
    judge = db.Column(db.Integer, nullable=False)
    correct_song_id = db.Column(db.Integer, nullable=False)
    select_song_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, game_id, question_num, judge, correct_song_id, select_song_id):
        self.game_id = game_id
        self.question_num = question_num
        self.judge = judge
        self.correct_song_id = correct_song_id
        self.select_song_id = select_song_id
        self.created_at = datetime.now()

    def __repr__(self):
        return '<Entry id:{}>'.format(self.id)
