from webapp.db import db


# Rutracker
class Torrent4(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    torrent_name = db.Column(db.String, nullable=False)
    torrent_date = db.Column(db.DateTime, nullable=False)
    torrent_size = db.Column(db.String, nullable=False)
    torrent_link = db.Column(db.String, nullable=False, unique=True)
    torrent_download_link = db.Column(db.String, unique=True, nullable=False)
    torrent_description = db.Column(db.String)

    def __repr__(self):
        return f'{self.torrent_name} {self.torrent_date} {self.torrent_size} {self.torrent_link} {self.torrent_download_link}'
