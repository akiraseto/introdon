from datetime import datetime

from introdon import db


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question1_correct_track_id = db.Column(db.Integer, nullable=False)
    question1_select1_track_id = db.Column(db.Integer, nullable=False)
    question1_select2_track_id = db.Column(db.Integer, nullable=False)
    question1_select3_track_id = db.Column(db.Integer, nullable=False)
    question1_select4_track_id = db.Column(db.Integer, nullable=False)

    question2_correct_track_id = db.Column(db.Integer, nullable=False)
    question2_select1_track_id = db.Column(db.Integer, nullable=False)
    question2_select2_track_id = db.Column(db.Integer, nullable=False)
    question2_select3_track_id = db.Column(db.Integer, nullable=False)
    question2_select4_track_id = db.Column(db.Integer, nullable=False)

    question3_correct_track_id = db.Column(db.Integer, nullable=False)
    question3_select1_track_id = db.Column(db.Integer, nullable=False)
    question3_select2_track_id = db.Column(db.Integer, nullable=False)
    question3_select3_track_id = db.Column(db.Integer, nullable=False)
    question3_select4_track_id = db.Column(db.Integer, nullable=False)

    question4_correct_track_id = db.Column(db.Integer, nullable=False)
    question4_select1_track_id = db.Column(db.Integer, nullable=False)
    question4_select2_track_id = db.Column(db.Integer, nullable=False)
    question4_select3_track_id = db.Column(db.Integer, nullable=False)
    question4_select4_track_id = db.Column(db.Integer, nullable=False)

    question5_correct_track_id = db.Column(db.Integer, nullable=False)
    question5_select1_track_id = db.Column(db.Integer, nullable=False)
    question5_select2_track_id = db.Column(db.Integer, nullable=False)
    question5_select3_track_id = db.Column(db.Integer, nullable=False)
    question5_select4_track_id = db.Column(db.Integer, nullable=False)

    question6_correct_track_id = db.Column(db.Integer, nullable=False)
    question6_select1_track_id = db.Column(db.Integer, nullable=False)
    question6_select2_track_id = db.Column(db.Integer, nullable=False)
    question6_select3_track_id = db.Column(db.Integer, nullable=False)
    question6_select4_track_id = db.Column(db.Integer, nullable=False)

    question7_correct_track_id = db.Column(db.Integer, nullable=False)
    question7_select1_track_id = db.Column(db.Integer, nullable=False)
    question7_select2_track_id = db.Column(db.Integer, nullable=False)
    question7_select3_track_id = db.Column(db.Integer, nullable=False)
    question7_select4_track_id = db.Column(db.Integer, nullable=False)

    question8_correct_track_id = db.Column(db.Integer, nullable=False)
    question8_select1_track_id = db.Column(db.Integer, nullable=False)
    question8_select2_track_id = db.Column(db.Integer, nullable=False)
    question8_select3_track_id = db.Column(db.Integer, nullable=False)
    question8_select4_track_id = db.Column(db.Integer, nullable=False)

    question9_correct_track_id = db.Column(db.Integer, nullable=False)
    question9_select1_track_id = db.Column(db.Integer, nullable=False)
    question9_select2_track_id = db.Column(db.Integer, nullable=False)
    question9_select3_track_id = db.Column(db.Integer, nullable=False)
    question9_select4_track_id = db.Column(db.Integer, nullable=False)

    question10_correct_track_id = db.Column(db.Integer, nullable=False)
    question10_select1_track_id = db.Column(db.Integer, nullable=False)
    question10_select2_track_id = db.Column(db.Integer, nullable=False)
    question10_select3_track_id = db.Column(db.Integer, nullable=False)
    question10_select4_track_id = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self,
                 question1_correct_track_id,
                 question1_select1_track_id,
                 question1_select2_track_id,
                 question1_select3_track_id,
                 question1_select4_track_id,
                 question2_correct_track_id,
                 question2_select1_track_id,
                 question2_select2_track_id,
                 question2_select3_track_id,
                 question2_select4_track_id,
                 question3_correct_track_id,
                 question3_select1_track_id,
                 question3_select2_track_id,
                 question3_select3_track_id,
                 question3_select4_track_id,
                 question4_correct_track_id,
                 question4_select1_track_id,
                 question4_select2_track_id,
                 question4_select3_track_id,
                 question4_select4_track_id,
                 question5_correct_track_id,
                 question5_select1_track_id,
                 question5_select2_track_id,
                 question5_select3_track_id,
                 question5_select4_track_id,
                 question6_correct_track_id,
                 question6_select1_track_id,
                 question6_select2_track_id,
                 question6_select3_track_id,
                 question6_select4_track_id,
                 question7_correct_track_id,
                 question7_select1_track_id,
                 question7_select2_track_id,
                 question7_select3_track_id,
                 question7_select4_track_id,
                 question8_correct_track_id,
                 question8_select1_track_id,
                 question8_select2_track_id,
                 question8_select3_track_id,
                 question8_select4_track_id,
                 question9_correct_track_id,
                 question9_select1_track_id,
                 question9_select2_track_id,
                 question9_select3_track_id,
                 question9_select4_track_id,
                 question10_correct_track_id,
                 question10_select1_track_id,
                 question10_select2_track_id,
                 question10_select3_track_id,
                 question10_select4_track_id,
                 user_id=None
                 ):
        self.question1_correct_track_id = question1_correct_track_id
        self.question1_select1_track_id = question1_select1_track_id
        self.question1_select2_track_id = question1_select2_track_id
        self.question1_select3_track_id = question1_select3_track_id
        self.question1_select4_track_id = question1_select4_track_id
        self.question2_correct_track_id = question2_correct_track_id
        self.question2_select1_track_id = question2_select1_track_id
        self.question2_select2_track_id = question2_select2_track_id
        self.question2_select3_track_id = question2_select3_track_id
        self.question2_select4_track_id = question2_select4_track_id
        self.question3_correct_track_id = question3_correct_track_id
        self.question3_select1_track_id = question3_select1_track_id
        self.question3_select2_track_id = question3_select2_track_id
        self.question3_select3_track_id = question3_select3_track_id
        self.question3_select4_track_id = question3_select4_track_id
        self.question4_correct_track_id = question4_correct_track_id
        self.question4_select1_track_id = question4_select1_track_id
        self.question4_select2_track_id = question4_select2_track_id
        self.question4_select3_track_id = question4_select3_track_id
        self.question4_select4_track_id = question4_select4_track_id
        self.question5_correct_track_id = question5_correct_track_id
        self.question5_select1_track_id = question5_select1_track_id
        self.question5_select2_track_id = question5_select2_track_id
        self.question5_select3_track_id = question5_select3_track_id
        self.question5_select4_track_id = question5_select4_track_id
        self.question6_correct_track_id = question6_correct_track_id
        self.question6_select1_track_id = question6_select1_track_id
        self.question6_select2_track_id = question6_select2_track_id
        self.question6_select3_track_id = question6_select3_track_id
        self.question6_select4_track_id = question6_select4_track_id
        self.question7_correct_track_id = question7_correct_track_id
        self.question7_select1_track_id = question7_select1_track_id
        self.question7_select2_track_id = question7_select2_track_id
        self.question7_select3_track_id = question7_select3_track_id
        self.question7_select4_track_id = question7_select4_track_id
        self.question8_correct_track_id = question8_correct_track_id
        self.question8_select1_track_id = question8_select1_track_id
        self.question8_select2_track_id = question8_select2_track_id
        self.question8_select3_track_id = question8_select3_track_id
        self.question8_select4_track_id = question8_select4_track_id
        self.question9_correct_track_id = question9_correct_track_id
        self.question9_select1_track_id = question9_select1_track_id
        self.question9_select2_track_id = question9_select2_track_id
        self.question9_select3_track_id = question9_select3_track_id
        self.question9_select4_track_id = question9_select4_track_id
        self.question10_correct_track_id = question10_correct_track_id
        self.question10_select1_track_id = question10_select1_track_id
        self.question10_select2_track_id = question10_select2_track_id
        self.question10_select3_track_id = question10_select3_track_id
        self.question10_select4_track_id = question10_select4_track_id

        self.user_id = user_id

        self.created_at = datetime.now()

    def __repr__(self):
        return '<Entry id:{}>'.format(self.id)
