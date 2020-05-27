from datetime import datetime

from introdon import db


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    game_id = db.Column(db.Integer, nullable=False)
    question_num = db.Column(db.Integer, nullable=False)
    judge = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer)
    correct_song_id = db.Column(db.Integer, nullable=False)
    select_song_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, game_id, question_num, judge, correct_song_id, select_song_id, user_id=None, score=0):
        self.user_id = user_id
        self.game_id = game_id
        self.question_num = question_num
        self.judge = judge
        self.score = score
        self.correct_song_id = correct_song_id
        self.select_song_id = select_song_id
        self.created_at = datetime.now()

    def __repr__(self):
        return '<Entry id:{} game_id:{} question_num:{} user_id:{} score:{}>'.format(self.id, self.game_id,
                                                                                     self.question_num, self.user_id,
                                                                                     self.score)


class LogLogic:
    def create_log(self, user_id: int, game_id: int, num: int, correct: int, answer: int, is_multi=False):
        judge = 0
        score = 0

        if answer == correct:
            judge = 1

            if is_multi:
                log_count = Log.query.filter(Log.game_id == game_id, Log.question_num == num, Log.judge == 1).count()

                if log_count == 0:
                    score = 50
                elif log_count == 1:
                    score = 40
                elif log_count == 2:
                    score = 30
                elif log_count == 3:
                    score = 20
                else:
                    score = 10

            else:
                score = 10

        this_log = Log(
            user_id=user_id,
            game_id=game_id,
            select_song_id=answer,
            judge=judge,
            score=score,
            question_num=num,
            correct_song_id=correct
        )
        db.session.add(this_log)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()

        return judge

    def calc_score(self, game_id: int, users_id_list: list):
        score_dict = {}
        for game_user in users_id_list:
            score_dict[game_user] = 0

        # 取得した参加user_idごとに得点を計算
        log_records = Log.query.filter(Log.game_id == game_id).all()
        for record in log_records:
            if record.user_id in users_id_list:
                score_dict[record.user_id] += record.score

        order_score = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)
        return order_score
