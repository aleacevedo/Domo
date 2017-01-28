from flask import flash, session, url_for,jsonify, abort, request, g
from flask_login import login_user, logout_user, current_user, login_required
from flask.ext.httpauth import HTTPBasicAuth
from app import app, db, lm, models

auth = HTTPBasicAuth()

@app.route('/IPs/api/v1.0/User', methods=['POST'])
def new_User():
    email = request.json.get('email')
    password = request.json.get('password')
    if email is None or password is None:
        print(email)
        print(password)
        abort(400)
    if models.User.query.filter_by(email = email).first() is not None:
        print("Email Repetido")
        abort(400)
    user = models.User(email = email)
    user.hash_passw(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'email': user.email}),201


@app.route('/IPs/api/v1.0/User/Disps', methods=['GET'])
@auth.login_required
def get_Disps():
    disps = {}
    for disp in models.Disp.query.filter_by(user_id=g.user.id).all():
        disps[disp.nickid] = disp.ip
        print(disp.ip)
    if(len(disps)==0):
        abort(404)
    return jsonify(disps)

@app.route('/IPs/api/v1.0/User/Disp', methods=['POST'])
@auth.login_required
def new_Disp():
    nickid = request.json.get('nickid')
    user_id = g.user.id
    if nickid is None or user_id is None:
        abort(400)
    disp = models.Disp.query.filter_by(user_id = user_id, nickid=nickid).first()
    if(disp is not None):
        abort(400)
    disp = models.Disp(nickid = nickid, user_id = user_id)
    db.session.add(disp)
    db.session.commit()
    return jsonify({'nickid': disp.nickid}), 201

@app.route('/IPs/api/v1.0/User/Disp/<nickid>', methods=['GET'])
@auth.login_required
def get_Disp(nickid):
    disp = models.Disp.query.filter_by(user_id=g.user.id,nickid=nickid).first()
    if(disp is None):
        abort(400)
    disp.ip = request.environ['REMOTE_ADDR']
    db.session.add(disp)
    db.session.commit()
    return jsonify({disp.nickid:disp.ip})

@app.route('/IPs/api/v1.0/User/Disp/<nickid>', methods=['PUT'])
@auth.login_required
def mod_Disp(nickid):
    disp = models.Disp.query.filter_by(user_id=g.user.id, nickid=nickid).first()
    if(disp is None):
        abort(400)
    nw_nickid = request.json.get('nickid')
    if(models.Disp.query.filter_by(user_id=g.user.id, nickid=nw_nickid).first() is not None):
        abort(400)
    disp.nickid = nw_nickid
    db.session.add(disp)
    db.session.commit()
    return jsonify({'nw':disp.nickid})

@auth.verify_password
def verify_password(email, password):
    user = models.User.query.filter_by(email = email).first()
    if not user or not user.verify_passw(password):
        return False
    g.user = user
    return True
