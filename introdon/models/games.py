from datetime import datetime

from introdon import db
from introdon.views.config_introdon import *


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

    @classmethod
    def create_game(cls, correct_id: list, select_id: list, user_id: int) -> tuple:
        """新規にGameを作成する

        1人目ユーザーの登録とともに、新規にGame作成し、game_id,作成日を返す

        ----------
        :param correct_id:  正解曲のIDリスト
        :param select_id: 選択曲のIDリスト
        :param user_id: ユーザーID
        :rtype: tuple(game_id:int, game_created_at:datetime)
        """

        records = {}
        for i in range(MAX_QUESTION):
            records["question" + str(i + 1) + "_correct_song_id"] = correct_id[i]
            for j in range(MAX_SELECT):
                records["question" + str(i + 1) + "_select" + str(j + 1) + "_song_id"] = select_id[i][j]

        if user_id:
            records["entry_user1"] = user_id

        this_game = Game(**records)
        db.session.add(this_game)
        try:
            db.session.commit()
        except:
            db.session.rollback()

        return this_game.id, this_game.created_at

    @classmethod
    def fetch_users_id(cls, game_instance: object) -> list:
        """ゲーム参加したuserのidを取得

        user_idをlistにして返す

        ----------
        :param game_instance: ゲームインスタンス
        """

        users_id_list = []
        for i in range(1, MAX_MEMBER + 1):
            attr_name = "entry_user" + str(i)
            user_id = getattr(game_instance, attr_name)
            if user_id != None:
                users_id_list.append(user_id)

        return users_id_list

    @classmethod
    def update_game(cls, order_score: list, game_instance: object) -> None:
        """Game内容を更新

        順位を追加して、GameのDBをupdate

        ----------
        :param order_score: ユーザーIDと得点のタプルが入ったリスト
        :param game_instance: ゲームインスタンス
        """

        grade_name = ['gold_user', 'silver_user', 'bronze_user']
        grade_score = ['gold_score', 'silver_score', 'bronze_score']

        for i, j in enumerate(order_score):
            setattr(game_instance, grade_name[i], j[0])
            setattr(game_instance, grade_score[i], j[1])

        game_instance.modified_at = datetime.now()
        db.session.add(game_instance)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    @classmethod
    def participate_in_game(cls, latest_game: object, user_id: int) -> None:
        """Gameにユーザーを参加登録する

        該当のGameインスタンスにユーザーを参加追加させる

        ----------
        :param latest_game: ゲームインスタンス
        :param user_id: ユーザーID
        """

        for i in range(1, MAX_MEMBER + 1):
            if not getattr(latest_game, 'entry_user' + str(i)):
                setattr(latest_game, 'entry_user' + str(i), user_id)
                break

        latest_game.modified_at = datetime.now()
        db.session.add(latest_game)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    @classmethod
    def fetch_songs_id(cls, latest_game: object) -> tuple:
        """正解曲と選択曲のsong_idのリストを取得

        Gameで使った正解/選択曲のidをそれぞれリストにしてタプルで返す

        ----------
        :param latest_game: ゲームインスタンス
        """

        correct_id = []
        select_id = [[0 for i in range(MAX_SELECT)] for j in range(MAX_QUESTION)]

        for i in range(MAX_QUESTION):
            attr_name = "question" + str(i + 1) + "_correct_song_id"
            id = getattr(latest_game, attr_name)
            correct_id.append(id)

            for j in range(MAX_SELECT):
                attr_name = "question" + str(i + 1) + "_select" + str(j + 1) + "_song_id"
                id = getattr(latest_game, attr_name)
                select_id[i][j] = id

        return correct_id, select_id
