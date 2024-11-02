from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
from models import db, Usuario
from flask_jwt_extended import jwt_required

login_bp = Blueprint('user', __name__)

@login_bp.route('/login', methods=['POST'])
@jwt_required()
def login():
    nome = request.json.get('nome', None)
    senha = request.json.get('senha', None)

    if not nome or not senha:
        return jsonify({'erro': 'Faltam dados'}), 400
    
    usuarios = Usuario.query.all()
    if not any(u.nome == nome and u.senha == senha for u in usuarios):
        return jsonify({'erro': 'Usuário ou senha inválidos'}), 401
    
    access_token = create_access_token(identity=nome)
    return jsonify(access_token=access_token), 200