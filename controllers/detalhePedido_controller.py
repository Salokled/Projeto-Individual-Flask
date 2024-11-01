from flask import Blueprint, request, jsonify
from models import db, Pedido, Produto, DetalhePedido

detalhePedido_bp = Blueprint('detalhePedido', __name__)

@detalhePedido_bp.route('/detalhePedido', methods=['POST'])
def criar_detalhe_pedidos():

    detalhepedido = request.json

    novo_detalhe_pedido = DetalhePedido(dp_quantidade=detalhepedido['dp_quantidade'],
                                        dp_preco=detalhepedido['dp_preco'],
                                        dp_desconto=detalhepedido['dp_desconto'],
                                        dp_pedido_id=detalhepedido['dp_pedido_id'],
                                        dp_produto_id=detalhepedido['dp_produto_id'])
    
    db.session.add(novo_detalhe_pedido)
    db.session.commit()

    return jsonify({'id': novo_detalhe_pedido.dp_id})

@detalhePedido_bp.route('/detalhePedido', methods=['GET'])
def listar_detalhe_pedidos():
    detalhes = DetalhePedido.query.all()
    return jsonify([{
        'id': d.dp_id,
        'quantidade': d.dp_quantidade,
        'preco': d.dp_preco,
        'desconto': d.dp_desconto,
        'pedido_id': d.dp_pedido_id,
        'produto_id': d.dp_produto_id
    } for d in detalhes]), 200

@detalhePedido_bp.route('/detalhePedido/<int:id>', methods=['PUT'])
def atualizar_detalhe_pedido(id):
    dados = request.json
    detalhe_pedido = DetalhePedido.query.get(id)

    if not detalhe_pedido:
        return jsonify({'Mensagem': 'Detalhe do pedido não encontrado'}), 404

    # Atualiza os campos conforme necessário
    detalhe_pedido.dp_quantidade = dados.get('dp_quantidade', detalhe_pedido.dp_quantidade)
    detalhe_pedido.dp_preco = dados.get('dp_preco', detalhe_pedido.dp_preco)
    detalhe_pedido.dp_desconto = dados.get('dp_desconto', detalhe_pedido.dp_desconto)

    db.session.commit()

    return jsonify({
        'id': detalhe_pedido.dp_id,
        'quantidade': detalhe_pedido.dp_quantidade,
        'preco': detalhe_pedido.dp_preco,
        'desconto': detalhe_pedido.dp_desconto
    }), 200

@detalhePedido_bp.route('/detalhePedido/<int:id>', methods=['DELETE'])
def deletar_detalhe_pedido(id):
    detalhe_pedido = DetalhePedido.query.get(id)

    if not detalhe_pedido:
        return jsonify({'Mensagem': 'Detalhe do pedido não encontrado'}), 404

    db.session.delete(detalhe_pedido)
    db.session.commit()

    return jsonify({'Mensagem': 'Detalhe do pedido deletado com sucesso'}), 200