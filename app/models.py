from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

class User(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),index=True, unique = True)
    email = db.Column(db.String(120),index=True, unique = True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Shift(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime, index=True)
    length = db.Column(db.Integer)
    user_1id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_2id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_3id = db.Column(db.Integer, db.ForeignKey('user.id'))