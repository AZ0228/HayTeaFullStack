from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

# reloads user object from the user ID stored in the session
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


user_shifts = db.Table('user_shifts',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('shift_id', db.Integer, db.ForeignKey('shift.id'))
)

class User(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),index=True, unique = True)
    email = db.Column(db.String(120),index=True, unique = True)
    password_hash = db.Column(db.String(128))
    shifts = db.relationship('Shift', secondary=user_shifts, backref='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Shift(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime, index=True)
    length = db.Column(db.Integer)