from datetime import datetime

from introdon import db


class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    artist = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    album = db.Column(db.String(255))
    jacket_img = db.Column(db.String(255))
    # preview = db.Column(db.String(255))
    preview = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, title=None, artist=None, genre=None, album=None, jacket_img=None, preview=None):
        self.title = title
        self.artist = artist
        self.genre = genre
        self.album = album
        self.jacket_img = jacket_img
        self.preview = preview
        self.created_at = datetime.utcnow()
        self.modified_at = datetime.utcnow()

    def __repr__(self):
        return '<Entry id:{} title:{} artist:{}>'.format(self.id, self.title, self.artist)
