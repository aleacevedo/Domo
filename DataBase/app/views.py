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

##USERS##

@app.route('/Data/api/v1.0/Users')
@auth.login_required
def get_users():
    allUsers = models.User.query.all()
    return jsonify(model_to_dict(allUsers))


@app.route('/Data/api/v1.0/User/<id>')
@auth.login_required
def get_user(id):
    user = models.User.query.filter_by(email=id).first()
    if not user:
        user = models.User.query.filter_by(nickName=id).first()
    if not user:
        abort(500)
    return jsonify(user)


@app.route('/Data/api/v1.0/User', methods=['POST'])
@auth.login_required
def add_user():
    if g.user.nickName != 'admin': abort(401)
    nickName = request.json['nickName']
    email = request.json['email']
    password = request.json['password']
    if models.User.query.filter_by(nickName=nickName).first() or models.User.query.filter_by(email=email).first():
        abort(500)
    nwUser = models.User(nickName=nickName, email=email)
    nwUser.mods = []
    nwUser.hash_password(password)
    db.session.add(nwUser)
    db.session.commit()
    return "OK", 200


@app.route('/Data/api/v1.0/User', methods=['PUT'])
@auth.login_required
def ch_user():
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
def del_user():
    db.session.delete(g.user)
    db.session.commit()
    return "OK", 200


@app.route('/Data/api/v1.0/User/mod', methods=['POST'])
@auth.login_required
def add_mod_to_user():
    idMod = request.json['idMod']
    if models.Mods.query.filter_by(id=idMod).first() is None:
        abort(500)
    if idMod not in g.user.mods:
        g.user.mods.append(idMod)
        db.session.add(g.user)
        db.session.commit()
        return "OK", 200
    abort(400)


@app.route('/Data/api/v1.0/User/mod', methods=['DELETE'])
@auth.login_required
def dell_mod_to_user():
    idMod = request.json['idMod']
    if models.Mods.query.filter_by(id=idMod).first() is None: abort(500)
    try:
        g.user.mods.remove(idMod)
        db.session.add(g.user)
        db.session.commit()
    except ValueError:
        abort(401)
    return "OK", 200


##MODULOS##
@app.route('/Data/api/v1.0/Mods')
@auth.login_required
def get_mods():
    return jsonify(model_to_dict(models.Mods.query.all()))


@app.route('/Data/api/v1.0/Mod/<id>')
@auth.login_required
def get_mod(id):
    if models.Mods.query.filter_by(id=id).first() is None: abort(500)
    return jsonify(models.Mods.query.filter_by(id=id).first())


@app.route('/Data/api/v1.0/Mod', methods=['POST'])
@auth.login_required
def add_mod():
    if g.user.nickName != 'admin':
        abort(401)
    try:
        uniqueID = request.json['uniqueID']
    except KeyError:
        abort(500)
    db.session.add(models.Mods(uniqueID=uniqueID, new=True, state=0))
    db.session.commit()
    return "OK", 200


@app.route('/Data/api/v1.0/Mod', methods=['DELETE'])
@auth.login_required
def del_mod():
    print("entro a delete")
    if g.user.nickName != 'admin':
        abort(401)
    if('idMod' in request.json):
        idMod = request.json['idMod']
        mod = models.Mods.query.filter_by(id=idMod).first()
    if('uniqueId' in request.json):
        uniqueId = request.json['uniqueId']
        mod = models.Mods.query.filter_by(uniqueID=idMod).first()
    if mod is None: abort(500)
    for user in models.User.query.all():
        if idMod in user.mods:
            user.mods.remove(idMod)
            db.session.add(user)
            db.session.commit()
    db.session.delete(mod)
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
