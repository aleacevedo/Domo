from flask import jsonify, abort, g, request
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


@app.route('/Data/api/v1.0/User', methods=['POST'])
@auth.login_required
def add_User():
    nickName = request.json['nickName']
    email = request.json['email']
    password = request.json['password']
    if models.User.query.filter_by(nickName=nickName).first() or models.User.query.filter_by(email=email).first():
        abort(500)
    nwUser = models.User(nickName=nickName, email=email)
    nwUser.hash_password(password)
    db.session.add(nwUser)
    db.session.commit()
    return "OK", 200


@app.route('/Data/api/v1.0/User', methods=['PUT'])
@auth.login_required
def ch_User():
    nickName = None
    email = None
    password = None
    userNick = None
    userEmail = None
    if 'nickName' in request.json:
        nickName = request.json['nickName']
        userNick = models.User.query.filter_by(nickName=nickName).first()
    if 'email' in request.json:
        email = request.json['email']
        userEmail = models.User.query.filter_by(email=email).first()
    if 'password' in request.json: password = request.json['password']
    if userEmail or userEmail:
        abort(500)
    g.user.ch(nickName=nickName, email=email, password=password)
    db.session.add(g.user)
    db.session.commit()
    return "OK", 200


@app.route('/Data/api/v1.0/User', methods=['DELETE'])
@auth.login_required
def del_User():
    db.session.delete(g.user)
    db.session.commit()
    return "OK", 200


@auth.verify_password
def verify_password(id, password):
    user = models.User.query.filter_by(email=id).first()
    if not user:
        user = models.User.query.filter_by(nickName=id).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True
