from app import db
from passlib.apps import custom_app_context as pwd_context

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), index = True, unique = True)
    nickName = db.Column(db.String(120), index = True, unique = True)
    password = db.Column(db.String(120))
    mods = db.relationship('Mods', backref = 'author', lazy = 'dynamic')

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def ch(self, nickName, email, password):
        if(nickName): self.nickName = nickName
        if(email): self.email = email
        if password: self.hash_password(password)

class Mods(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickName = db.Column(db.String(120), index=True)
    uniqueID = db.Column(db.Integer, unique = True)
    state = db.Column(db.Integer)
    new = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
