from app import db, sched, mqtt
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.ext.mutable import MutableList


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    nickName = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120))
    mods = db.Column(MutableList.as_mutable(db.PickleType()))

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def ch(self, nickName, email, password):
        if(nickName): self.nickName = nickName
        if(email): self.email = email
        if password: self.hash_password(password)


class Mods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickName = db.Column(db.String(120), index=True)
    uniqueID = db.Column(db.Integer, unique=True)
    ip = db.Column(db.String(12), unique=True)
    state = db.Column(db.Integer)
    new = db.Column(db.Boolean)
    tasks = db.relationship('Task')

    def execute_change(self, newState):
        self.state = newState
        mqtt.send_to(self.uniqueID, self.state)



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickName = db.Column(db.Integer)
    hour = db.Column(db.Integer)
    minute = db.Column(db.Integer)
    wDay = db.Column(db.Integer)
    newState = db.Column(db.Integer)
    idMod = db.Column(db.Integer, db.ForeignKey('mods.id'))

    def save(self, mod):
        sched.add_job(
            lambda: mod.execute_change(self.newState),
            "cron",
            day_of_week=self.wDay,
            hour=self.hour,
            minute=self.minute,
            id=self.id,
            replace_existing = True
        )

    def delete(self):
        sched.remove_job(self.id)
