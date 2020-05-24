import random
from datetime import datetime

from introdon import db, ma
from introdon.views.config_introdon import MAX_QUESTION, MAX_SELECT


class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    track = db.Column(db.String(255), nullable=False)
    track_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    artist_id = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(255))
    jacket_img = db.Column(db.String(255), nullable=False)
    preview = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, track, track_id, artist, artist_id, jacket_img, preview, genre=None, release_date=None, ):
        self.track = track
        self.track_id = track_id
        self.artist = artist
        self.artist_id = artist_id
        self.genre = genre
        self.jacket_img = jacket_img
        self.preview = preview
        self.release_date = release_date
        self.created_at = datetime.now()
        self.modified_at = datetime.now()

    def __repr__(self):
        return '<Entry id:{} track:{} artist:{}>'.format(self.id, self.track, self.artist)


class SongLogic():
    def __init__(self):
        self.validate = False
        self.flash = ''
        self.correct_id = []
        self.select_id = []

    def make_question(self, artist, genre, release_from, release_end):
        release_from = datetime.strptime(release_from, '%Y')
        release_end = datetime.strptime(release_end, '%Y')

        song_instance = Song.query.with_entities(Song.id).filter(Song.artist.like('%' + artist + '%'),
                                                                 Song.genre.like('%' + genre + '%'),
                                                                 Song.release_date >= release_from,
                                                                 Song.release_date < release_end).all()
        song_instance = [value[0] for value in song_instance]

        # レコード数をカウント
        songs_count = len(song_instance)

        # 登録曲が少なすぎる場合
        if songs_count < MAX_QUESTION * 4:

            self.validate = False
            self.flash = '該当曲が少なくて問題を作れません、範囲を広めてください。'
            return self.validate

        else:
            self.validate = True
            self.flash = ''
            # 正解を作る
            correct_id = []
            for i in range(MAX_QUESTION):
                while True:
                    index = random.randint(0, songs_count - 1)
                    if index not in correct_id:
                        correct_id.append(index)
                        break
            correct_id = [song_instance[i] for i in correct_id]

            # 選択肢を作成
            select_id = [[0 for i in range(MAX_SELECT)] for j in range(MAX_QUESTION)]

            for i in range(MAX_QUESTION):
                rand_index = random.randint(0, MAX_SELECT - 1)
                select_id[i][rand_index] = correct_id[i]
                for j in range(MAX_SELECT):
                    if select_id[i][j] == 0:
                        while True:
                            index = song_instance[random.randint(0, songs_count - 1)]
                            if index not in select_id[i]:
                                select_id[i][j] = index

                                break

            self.correct_id = correct_id
            self.select_id = select_id

        return self.validate

    def dump_question_song(self, correct, selects, num):
        song_schema = SongSchema()
        correct_song = song_schema.dump(Song.query.filter(Song.id == correct[num - 1]).first())
        select_songs = song_schema.dump(Song.query.filter(Song.id.in_(selects[num - 1])).all(), many=True)

        return correct_song, select_songs

    def dump_correct_songs_list(self, correct_songs):
        correct_song_list = Song.query.filter(Song.id.in_(correct_songs)).all()
        correct_song_list = [next(s for s in correct_song_list if s.id == id) for id in correct_songs]

        song_schema = SongSchema()
        correct_song_list = song_schema.dump(correct_song_list, many=True)

        return correct_song_list


class SongSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Song
