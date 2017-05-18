from flask import jsonify, abort, g
from flask.ext.httpauth import HTTPBasicAuth
from app import app, db, models

auth = HTTPBasicAuth()


def model_to_dict(model):
    dict = {}
    for x in model:
        x = x.__dict__
        del x['_sa_instance_state']
        dict[x['nickName']] = x
    return dict


@app.route('/Data/api/v1.0/Users')
@auth.login_required
def get_Users():
    allUsers = models.User.query.all()
    return jsonify(model_to_dict(allUsers))


@app.route('/Data/api/v1.0/User/<id>')
@auth.login_required
def get_User(id):
    user = models.User.query.filter_by(email=id).first()
    if not user:
        user = models.User.query.filter_by(nickName=id).first()
    if not user:
        abort(500)
    return jsonify(user)


@auth.verify_password
def verify_password(id, password):
    user = models.User.query.filter_by(email=id).first()
    if not user:
        user = models.User.query.filter_by(nickName=id).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True
