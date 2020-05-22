from datetime import datetime

from introdon import db
from introdon.views.config_introdon import MAX_QUESTION, MAX_SELECT


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question1_correct_song_id = db.Column(db.Integer, nullable=False)
    question1_select1_song_id = db.Column(db.Integer, nullable=False)
    question1_select2_song_id = db.Column(db.Integer, nullable=False)
    question1_select3_song_id = db.Column(db.Integer, nullable=False)
    question1_select4_song_id = db.Column(db.Integer, nullable=False)

    question2_correct_song_id = db.Column(db.Integer, nullable=False)
    question2_select1_song_id = db.Column(db.Integer, nullable=False)
    question2_select2_song_id = db.Column(db.Integer, nullable=False)
    question2_select3_song_id = db.Column(db.Integer, nullable=False)
    question2_select4_song_id = db.Column(db.Integer, nullable=False)

    question3_correct_song_id = db.Column(db.Integer, nullable=False)
    question3_select1_song_id = db.Column(db.Integer, nullable=False)
    question3_select2_song_id = db.Column(db.Integer, nullable=False)
    question3_select3_song_id = db.Column(db.Integer, nullable=False)
    question3_select4_song_id = db.Column(db.Integer, nullable=False)

    question4_correct_song_id = db.Column(db.Integer, nullable=False)
    question4_select1_song_id = db.Column(db.Integer, nullable=False)
    question4_select2_song_id = db.Column(db.Integer, nullable=False)
    question4_select3_song_id = db.Column(db.Integer, nullable=False)
    question4_select4_song_id = db.Column(db.Integer, nullable=False)

    question5_correct_song_id = db.Column(db.Integer, nullable=False)
    question5_select1_song_id = db.Column(db.Integer, nullable=False)
    question5_select2_song_id = db.Column(db.Integer, nullable=False)
    question5_select3_song_id = db.Column(db.Integer, nullable=False)
    question5_select4_song_id = db.Column(db.Integer, nullable=False)

    question6_correct_song_id = db.Column(db.Integer, nullable=False)
    question6_select1_song_id = db.Column(db.Integer, nullable=False)
    question6_select2_song_id = db.Column(db.Integer, nullable=False)
    question6_select3_song_id = db.Column(db.Integer, nullable=False)
    question6_select4_song_id = db.Column(db.Integer, nullable=False)

    question7_correct_song_id = db.Column(db.Integer, nullable=False)
    question7_select1_song_id = db.Column(db.Integer, nullable=False)
    question7_select2_song_id = db.Column(db.Integer, nullable=False)
    question7_select3_song_id = db.Column(db.Integer, nullable=False)
    question7_select4_song_id = db.Column(db.Integer, nullable=False)

    question8_correct_song_id = db.Column(db.Integer, nullable=False)
    question8_select1_song_id = db.Column(db.Integer, nullable=False)
    question8_select2_song_id = db.Column(db.Integer, nullable=False)
    question8_select3_song_id = db.Column(db.Integer, nullable=False)
    question8_select4_song_id = db.Column(db.Integer, nullable=False)

    question9_correct_song_id = db.Column(db.Integer, nullable=False)
    question9_select1_song_id = db.Column(db.Integer, nullable=False)
    question9_select2_song_id = db.Column(db.Integer, nullable=False)
    question9_select3_song_id = db.Column(db.Integer, nullable=False)
    question9_select4_song_id = db.Column(db.Integer, nullable=False)

    question10_correct_song_id = db.Column(db.Integer, nullable=False)
    question10_select1_song_id = db.Column(db.Integer, nullable=False)
    question10_select2_song_id = db.Column(db.Integer, nullable=False)
    question10_select3_song_id = db.Column(db.Integer, nullable=False)
    question10_select4_song_id = db.Column(db.Integer, nullable=False)

    entry_user1 = db.Column(db.Integer)
    entry_user2 = db.Column(db.Integer)
    entry_user3 = db.Column(db.Integer)
    entry_user4 = db.Column(db.Integer)
    entry_user5 = db.Column(db.Integer)

    gold_user = db.Column(db.Integer)
    silver_user = db.Column(db.Integer)
    bronze_user = db.Column(db.Integer)

    gold_score = db.Column(db.Integer)
    silver_score = db.Column(db.Integer)
    bronze_score = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self,
                 question1_correct_song_id,
                 question1_select1_song_id,
                 question1_select2_song_id,
                 question1_select3_song_id,
                 question1_select4_song_id,
                 question2_correct_song_id,
                 question2_select1_song_id,
                 question2_select2_song_id,
                 question2_select3_song_id,
                 question2_select4_song_id,
                 question3_correct_song_id,
                 question3_select1_song_id,
                 question3_select2_song_id,
                 question3_select3_song_id,
                 question3_select4_song_id,
                 question4_correct_song_id,
                 question4_select1_song_id,
                 question4_select2_song_id,
                 question4_select3_song_id,
                 question4_select4_song_id,
                 question5_correct_song_id,
                 question5_select1_song_id,
                 question5_select2_song_id,
                 question5_select3_song_id,
                 question5_select4_song_id,
                 question6_correct_song_id,
                 question6_select1_song_id,
                 question6_select2_song_id,
                 question6_select3_song_id,
                 question6_select4_song_id,
                 question7_correct_song_id,
                 question7_select1_song_id,
                 question7_select2_song_id,
                 question7_select3_song_id,
                 question7_select4_song_id,
                 question8_correct_song_id,
                 question8_select1_song_id,
                 question8_select2_song_id,
                 question8_select3_song_id,
                 question8_select4_song_id,
                 question9_correct_song_id,
                 question9_select1_song_id,
                 question9_select2_song_id,
                 question9_select3_song_id,
                 question9_select4_song_id,
                 question10_correct_song_id,
                 question10_select1_song_id,
                 question10_select2_song_id,
                 question10_select3_song_id,
                 question10_select4_song_id,
                 entry_user1=None
                 ):
        self.question1_correct_song_id = question1_correct_song_id
        self.question1_select1_song_id = question1_select1_song_id
        self.question1_select2_song_id = question1_select2_song_id
        self.question1_select3_song_id = question1_select3_song_id
        self.question1_select4_song_id = question1_select4_song_id
        self.question2_correct_song_id = question2_correct_song_id
        self.question2_select1_song_id = question2_select1_song_id
        self.question2_select2_song_id = question2_select2_song_id
        self.question2_select3_song_id = question2_select3_song_id
        self.question2_select4_song_id = question2_select4_song_id
        self.question3_correct_song_id = question3_correct_song_id
        self.question3_select1_song_id = question3_select1_song_id
        self.question3_select2_song_id = question3_select2_song_id
        self.question3_select3_song_id = question3_select3_song_id
        self.question3_select4_song_id = question3_select4_song_id
        self.question4_correct_song_id = question4_correct_song_id
        self.question4_select1_song_id = question4_select1_song_id
        self.question4_select2_song_id = question4_select2_song_id
        self.question4_select3_song_id = question4_select3_song_id
        self.question4_select4_song_id = question4_select4_song_id
        self.question5_correct_song_id = question5_correct_song_id
        self.question5_select1_song_id = question5_select1_song_id
        self.question5_select2_song_id = question5_select2_song_id
        self.question5_select3_song_id = question5_select3_song_id
        self.question5_select4_song_id = question5_select4_song_id
        self.question6_correct_song_id = question6_correct_song_id
        self.question6_select1_song_id = question6_select1_song_id
        self.question6_select2_song_id = question6_select2_song_id
        self.question6_select3_song_id = question6_select3_song_id
        self.question6_select4_song_id = question6_select4_song_id
        self.question7_correct_song_id = question7_correct_song_id
        self.question7_select1_song_id = question7_select1_song_id
        self.question7_select2_song_id = question7_select2_song_id
        self.question7_select3_song_id = question7_select3_song_id
        self.question7_select4_song_id = question7_select4_song_id
        self.question8_correct_song_id = question8_correct_song_id
        self.question8_select1_song_id = question8_select1_song_id
        self.question8_select2_song_id = question8_select2_song_id
        self.question8_select3_song_id = question8_select3_song_id
        self.question8_select4_song_id = question8_select4_song_id
        self.question9_correct_song_id = question9_correct_song_id
        self.question9_select1_song_id = question9_select1_song_id
        self.question9_select2_song_id = question9_select2_song_id
        self.question9_select3_song_id = question9_select3_song_id
        self.question9_select4_song_id = question9_select4_song_id
        self.question10_correct_song_id = question10_correct_song_id
        self.question10_select1_song_id = question10_select1_song_id
        self.question10_select2_song_id = question10_select2_song_id
        self.question10_select3_song_id = question10_select3_song_id
        self.question10_select4_song_id = question10_select4_song_id

        self.entry_user1 = entry_user1

        self.created_at = datetime.now()
        self.modified_at = datetime.now()

    def __repr__(self):
        return '<Entry id:{}>'.format(self.id)


class GameLogic:
    def __init__(self):
        self.game_id = None

    def create_game(self, correct_id: int, select_id: int, user_id: int):
        # song_idにしてGame tableに保存
        records = {}
        for i in range(MAX_QUESTION):
            records["question" + str(i + 1) + "_correct_song_id"] = correct_id[i]
            for j in range(MAX_SELECT):
                records["question" + str(i + 1) + "_select" + str(j + 1) + "_song_id"] = select_id[i][j]

        if user_id:
            records["entry_user1"] = user_id

        this_game = Game(**records)
        db.session.add(this_game)
        db.session.commit()

        self.game_id = this_game.id
        return self.game_id
