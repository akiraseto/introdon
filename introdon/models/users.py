import traceback
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
    sum_score = db.Column(db.Integer)
    rate = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, username, password, admin=0, sum_game=0, sum_answer=0, sum_correct=0, sum_score=0, rate=0):
        self.username = username
        self.password = password
        self.admin = admin
        self.sum_game = sum_game
        self.sum_answer = sum_answer
        self.sum_correct = sum_correct
        self.sum_score = sum_score
        self.rate = rate
        self.created_at = datetime.now()
        self.modified_at = datetime.now()

    def __repr__(self):
        return '<Entry id:{} username:{}>'.format(self.id, self.username)

    @classmethod
    def bind_name_score(cls, users_id_list: list, order_score: list) -> list:
        """Usernameとscoreをセットにする

        scoreが高い順にソートして、ユーザー名とマッピングしたリストを返す

        ----------
        :param users_id_list: 参加ユーザーのIDリスト
        :param order_score: ユーザーIDとスコア合計のマッピングリスト
        """

        user_id_name = User.query.with_entities(User.id, User.username).filter(User.id.in_(users_id_list)).order_by(
            User.id).all()
        display_rank = {name: value for id, name in user_id_name for id2, value in order_score if id == id2}
        display_rank = sorted(display_rank.items(), key=lambda x: x[1], reverse=True)

        return display_rank

    @classmethod
    def add_record_to_user(cls, judge: int, user_id: int, num: int, score: int) -> bool:
        """logの成績をユーザーに追加する

        Userの得点、ゲーム数、回答数、正解数、正解率を追加変更する

        ----------
        :param judge: 正解したか
        :param user_id: ユーザーID
        :param num: 何問目
        :param score: 獲得スコア
        :return: bool
        """

        validate = False
        if user_id:
            update_user = User.query.filter(User.id == user_id).first()
            update_user.sum_answer += 1

            if num == 10:
                update_user.sum_game += 1

            if judge:
                update_user.sum_correct += 1
                update_user.sum_score += score

            try:
                rate = round(update_user.sum_correct / update_user.sum_answer, 2)
            except Exception as e:
                rate = 0

            update_user.rate = rate
            update_user.modified_at = datetime.now()

            db.session.add(update_user)
            try:
                db.session.commit()
                validate = True
            except:
                db.session.rollback()
                traceback.print_exc()

        return validate

    @classmethod
    def fetch_user_records(cls, users_id_list: list) -> list:
        """ユーザーの累積成績を返す

        user_idリストを渡すと、各ユーザーの成績をlistにして返す

        ----------
        :param users_id_list: ユーザーIDリスト
        """

        users_record_list = User.query.with_entities(
            User.username,
            User.sum_score,
            User.rate,
        ).filter(User.id.in_(users_id_list)).all()

        return users_record_list
