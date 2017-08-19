import atexit
from flask import Flask, request, render_template
import paho.mqtt.publish as pub
from apscheduler.schedulers.background import BackgroundScheduler
from wtforms import Form, StringField, validators, IntegerField



app = Flask(__name__)


@app.route("/")
def main():
    return render_template('main.html')

@app.route("/<topic>/<pin>")
def action(topic, pin):
    triggerPin(pin, topic)
    return render_template('main.html')


@app.route('/addTask', methods=['GET', 'POST'])
def addTask():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        sched.add_job(
            lambda: triggerPin(form.pin.data,form.state.data),
            "cron",
            day_of_week=form.day.data,
            hour=form.hour.data,
            minute=form.minute.data,
            id=form.id.data,
            replace_existing = True
        )
        return render_template("main.html")
    return render_template('addTask.html', form=form)


@app.route("/listTasks")
def listTasks():
    tasks = sched.get_jobs()
    return render_template("listTasks.html", data=tasks)

if __name__ == "__main__":

    sched = BackgroundScheduler()
    class RegistrationForm(Form):
        days = ["mon","tue","wed","thu","fri","sat","sun"]
        pins = [0,2,4,5]
        states = ["turnOn", "turnOff"]
        day = StringField('day', [validators.AnyOf(days)])
        hour = IntegerField('hour', [validators.NumberRange(0,23)])
        minute = IntegerField('minute', [validators.number_range(0,59)])
        id = StringField('id', [validators.Length(5,15)])
        description = StringField('description', [validators.Length(0,55)])
        pin = IntegerField('pin', [validators.AnyOf(pins)])
        state = StringField('state', [validators.AnyOf(states)])

    def triggerPin(pin, topic):
        pub.single(topic, pin, hostname="192.168.0.247")

    sched.start()

    app.run(debug=True, host='0.0.0.0', threaded=True)
    atexit.register(lambda: sched.shutdown())
