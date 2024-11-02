from flask import Blueprint, request, jsonify
from models import db, Usuario
from flask_jwt_extended import jwt_required

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/usuario', methods=['POST'])

def criar_usuario():
    dados = request.json
    if not all(key in dados for key in ('nome', 'senha')):
        return jsonify({'erro': 'Faltam dados'}), 400

    novo_usuario = Usuario(nome=dados['nome'], senha=dados['senha'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'id': novo_usuario.id, 'nome': novo_usuario.nome}), 201

@usuario_bp.route('/usuario', methods=['GET'])
@jwt_required()
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{'id': u.id, 'nome': u.nome} for u in usuarios]), 200

@usuario_bp.route('/usuario/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_usuario(id):
    dados = request.json

    if not any(key in dados for key in ('nome', 'senha')):
        return jsonify({'erro': 'Faltam dados'}), 400
    
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    usuario.nome = '' + dados.get('nome', usuario.nome)
    usuario.senha = '' + dados.get('senha', usuario.senha)
    db.session.commit()
    return jsonify({'id': usuario.id, 'nome': usuario.nome}), 200

@usuario_bp.route('/usuario/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_usuario(id):
    usuario = Usuario.query.get(id)
    
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário deletado com sucesso'}), 200