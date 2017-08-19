
import atexit
from config import basedir
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
sched = BackgroundScheduler()
sched.start()
atexit.register(lambda: sched.shutdown())

from app import views, models
