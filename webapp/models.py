from webapp.db import db


class Torrent(db.Model):
    id = db.Column(db.Iteger, primary_key=True)
    torrent_name = db.Column(db.String, nullable=False)
    torrent_date = db.Column(db.DateTime, nullable=False)
    torrent_size = db.Column(db.String, nullable=False)
    torrent_file_link = db.Column(db.String, nullable=False)
