from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
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


# Authorization
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def _repr_(self):
        return f'<User name={self.username} id={self.id}>'
