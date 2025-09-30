"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api, resources={r"/api/*": {"origins": "*"}})


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route('/login', methods=['POST'])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    if not email:
        return jsonify({"error": "El email es requerido"}), 400

    if not password:
        return jsonify({"error": "La contraseña es requerida"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Credenciales invalidas"}), 401

    if not check_password_hash(user.password, password):
        return jsonify({"error": "Credenciales invalidas"}), 401

    expires = datetime.timedelta(hours=1)

    access_token = create_access_token(
        identity=str(user.id), expires_delta=expires)

    data = {
        "access_token": access_token,
        "user": user.serialize()
    }

    return jsonify(data), 200


@api.route('/register', methods=['POST'])
def register():
    email = request.json.get("email")
    password = request.json.get("password")

    if not email:
        return jsonify({"error": "El email es requerido"}), 400

    if not password:
        return jsonify({"error": "La contraseña es requerida"}), 400

    found = User.query.filter_by(email=email).first()

    if found:
        return jsonify({"error": "El email ya esta siendo utilizado"}), 400

    user = User()
    user.email = email
    user.password = generate_password_hash(password)
    user.is_active = True

    db.session.add(user)
    db.session.commit()

    return jsonify({"success": "Registro exitoso"}), 200


@api.route('/private', methods=['GET'])
@jwt_required()
def private():
    id = get_jwt_identity()

    user = User.query.get(id)

    return jsonify({"success": "ESTAS DENTRO!"}), 200
