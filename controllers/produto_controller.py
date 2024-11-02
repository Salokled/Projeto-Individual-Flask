from flask import Blueprint, request, jsonify
from models import db, Produto
from flask_jwt_extended import jwt_required

produto_bp = Blueprint('produto', __name__)

@produto_bp.route('/produto', methods=['POST'])
@jwt_required()
def criar_produto():
    dados = request.json
    novo_produto = Produto(nome=dados['nome'])
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify({'id': novo_produto.id, 'nome': novo_produto.nome, 'categoria_id': novo_produto.categoria_id}), 201

@produto_bp.route('/produto', methods=['GET'])
@jwt_required()
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([{'id': p.id, 'nome': p.nome, 'categoria_id': p.categoria_id} for p in produtos]), 200

@produto_bp.route('/produto/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_produto(id):
    dados = request.json
    produto = Produto.query.get(id)
    
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    produto.nome = dados['nome']
    db.session.commit()
    return jsonify({'id': produto.id, 'nome': produto.nome, 'categoria_id': produto.categoria_id}), 200

@produto_bp.route('/produto/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_produto(id):
    produto = Produto.query.get(id)
    
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'mensagem': 'Produto deletado com sucesso'}), 200
