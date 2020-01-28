from datetime import datetime

from introdon import db


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

    def __init__(self, track=None, track_id=None, artist=None, artist_id=None, genre=None, release_date=None,
                 jacket_img=None, preview=None):
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
