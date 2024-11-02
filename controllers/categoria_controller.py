from flask import Blueprint, request, jsonify
from models import db, Categoria
from flask_jwt_extended import jwt_required

categoria_bp = Blueprint('categoria', __name__)

@categoria_bp.route('/categoria', methods=['POST'])
@jwt_required()
def criar_categoria():
    dados = request.json
    if 'nome' not in dados:
        return jsonify({'erro': 'Faltam dados'}), 400

    nova_categoria = Categoria(nome=dados['nome'])
    db.session.add(nova_categoria)
    db.session.commit()
    return jsonify({'id': nova_categoria.id, 'nome': nova_categoria.nome}), 201

@categoria_bp.route('/categoria', methods=['GET'])
@jwt_required()
def listar_categorias():
    categorias = Categoria.query.all()
    return jsonify([{'id': u.id, 'nome': u.nome} for u in categorias]), 200

@categoria_bp.route('/categoria/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_categoria(id):
    dados = request.json

    if 'nome' not in dados:
        return jsonify({'erro': 'Faltam dados'}), 400
    
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({'erro': 'Categoria não encontrada'}), 404
    
    categoria.nome = '' + dados.get('nome', categoria.nome)
    db.session.commit()
    return jsonify({'id': categoria.id, 'nome': categoria.nome}), 200

@categoria_bp.route('/categoria/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_categoria(id):
    categoria = Categoria.query.get(id)
    
    if not categoria:
        return jsonify({'erro': 'Categoria não encontrada'}), 404
    
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({'mensagem': 'Categoria deletada com sucesso'}), 200