from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Rutracker
class Torrent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    torrent_name = db.Column(db.String, nullable=False)
    torrent_date = db.Column(db.DateTime, nullable=False)
    torrent_size = db.Column(db.String, nullable=False)
    torrent_file_link = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'{self.torrent_name} {self.torrent_date} {self.torrent_size} {self.torrent_file_link}'


class Torrent_description(db.Model):
    id = db.Column(db.Integer, primary_key=True)
