from app import db
from passlib.apps import custom_app_context as pwd_context

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    passw = db.Column(db.String(128))
    disp = db.relationship('Disp', backref='author', lazy='dynamic')

    def hash_passw(self, password):
        self.passw = pwd_context.encrypt(password)

    def verify_passw(self, password):
        return pwd_context.verify(password, self.passw)



class Disp(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickid = db.Column(db.String(120), index=True)
    ip = db.Column(db.String(120), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
