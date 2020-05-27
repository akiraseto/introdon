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


class UserLogic():
    def bind_name_score(self, users_id_list, order_score):
        """Usernameとscoreをセットにする

        scoreが高い順にソートしたリストを返す
        :rtype: list
        """
        user_id_name = User.query.with_entities(User.id, User.username).filter(User.id.in_(users_id_list)).order_by(
            User.id).all()
        display_rank = {name: value for id, name in user_id_name for id2, value in order_score if id == id2}
        display_rank = sorted(display_rank.items(), key=lambda x: x[1], reverse=True)

        return display_rank

    def add_score_to_user(self, user_id: int, score: int):
        """スコアをユーザーに追加する

        logの得点をユーザーの総得点に追加する

        ----------
        :return: bool
        """

        validate = False
        if user_id:
            update_user = User.query.filter(User.id == user_id).first()
            update_user.sum_score += score
            db.session.add(update_user)
            try:
                db.session.commit()
                validate = True
            except:
                db.session.rollback()
                raise

        return validate
