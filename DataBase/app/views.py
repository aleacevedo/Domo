from flask  import jsonify, abort, request, g
from flask.ext.httpauth import HTTPBasicAuth
from app import app, db, models

auth = HTTPBasicAuth()

@app.route('/Data/api/v1.0/Users')
@auth.login_required
def get_Users():
    users = {}
    allUsers = models.User.query.all()
    for user in allUsers:
        users[allUsers['eMail']] = user
    return jsonify(users)

@app.route('/Data/api/v1.0/User/<id>')
@auth.login_required
def get_User(id):
    user = None
    #user = model.User.query.filter_by(eMail = id or nickName = id).first()
    if(not user):
        abort(500)
    return jsonify(user)

@auth.verify_password
def verify_password(id, password):
    user = None
    #user = models.User.query.filter_by(eMail = id or nickName = id).first
    if(not user or not user.verify_password(password)):
        return False
    g.user = user
    return True
