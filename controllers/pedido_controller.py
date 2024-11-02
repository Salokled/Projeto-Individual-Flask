from flask import Blueprint, request, jsonify
from models import db, Pedido, Produto
from flask_jwt_extended import jwt_required

pedido_bp = Blueprint('pedido', __name__)

@pedido_bp.route('/pedidos', methods=['POST'])
@jwt_required()
def criar_pedido():
    dados = request.json
    if not all(key in dados for key in ('produto', 'valor', 'desconto')):
        return jsonify({'erro': 'Faltam dados'}), 400
    
    produtos = Produto.query.all()
    produtos_id = [p.id for p in produtos]
    if dados['produto_id'] not in produtos_id:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    novo_pedido = Pedido(produto_id=dados['produto_id'], quantidade=dados['quantidade'], usuario_id=dados['usuario_id'], status=dados['status'])
    db.session.add(novo_pedido)
    db.session.commit()
    return jsonify({'id': novo_pedido.id, 'produto_id': novo_pedido.produto_id, 'quantidade': novo_pedido.quantidade, 'usuario_id': novo_pedido.usuario_id, 'status': novo_pedido.status}), 201

@pedido_bp.route('/pedidos', methods=['GET'])
@jwt_required()
def listar_pedidos():
    pedidos = Pedido.query.all()
    return jsonify([{'id': pedidos.id, 'valor': pedidos.valor, 'desconto': pedidos.desconto} for p in pedidos]), 200

@pedido_bp.route('/pedidos/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_pedido(id):
    dados = request.json
    pedido = Pedido.query.get(id)
    
    if not pedido:
        return jsonify({'erro': 'Pedido não encontrado'}), 404
    
    pedido.valor = dados['valor']
    pedido.desconto = dados['desconto']
    pedido.status = dados['status']
    db.session.commit()
    return jsonify({'id': pedido.id, 'valor': pedido.valor, 'desconto': pedido.desconto}), 200

@pedido_bp.route('/pedidos/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_pedido(id):
    pedido = Pedido.query.get(id)
    
    if not pedido:
        return jsonify({'erro': 'Pedido não encontrado'}), 404
    
    db.session.delete(pedido)
    db.session.commit()
    return jsonify({'mensagem': 'Pedido deletado com sucesso'}), 200