from datetime import datetime
from enum import unique
from flask_login import UserMixin
from sqlalchemy.orm import backref
from url_shortener_app import db, bcrypt, login_manager


@login_manager.user_loader
def load_user(creator_id):
    return Creator.query.get(int(creator_id))

class Creator(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=250), nullable=False)
    email = db.Column(db.String(length=255), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    urls = db.relationship('ShortUrl', backref='urls', lazy=True)

    @property
    def password(self):
        return self.password

    def password_length(self):
        return len(self.password)

    @password.setter
    def password(self,plain_password):
        self.password_hash = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def check_password(self, attempted_password):
        if (bcrypt.check_password_hash(self.password_hash, attempted_password)):
            return True


class ShortUrl(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), nullable=False)
    original_url = db.Column(db.String(length=3000), nullable=False)
    created_at = db.Column(db.Date(), default=datetime.now())
    creator_id = db.Column(db.Integer(), db.ForeignKey('creator.id'))
    creator = db.relationship('Creator', backref='creator', lazy=True)

    @property
    def shortened_url(self):
        BASE62 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        number = self.id
        res = ""
        while number > 0:
            res += BASE62[number%62]
            number = number // 62
        return res[::-1]
