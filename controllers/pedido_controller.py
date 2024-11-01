from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Pedido, Cliente, DetalhePedido


# instância(objeto) de Blueprint
pedido_bp = Blueprint('pedidos', __name__)

# Decorator da rota pedidos, que é do tipo POST (enviando dados)
from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Pedido

# Instância(objeto) de Blueprint para pedidos
pedido_bp = Blueprint('pedidos', __name__)

# @pedido_bp.route('/pedidos', methods=['POST'])
# def criar_pedido():
#     pedido = request.json
#     _data_compra = datetime.strptime(pedido['data_compra'], '%Y-%m-%d').date()
#     novo_pedido = Pedido(data_compra=_data_compra, cliente_id=pedido['cliente_id'])
#     db.session.add(novo_pedido)
#     db.session.commit()
#     return jsonify({'id': novo_pedido.pedido_id, 'data_compra': novo_pedido.data_compra}), 201
# Instância(objeto) de Blueprint para pedidos
#pedido_bp = Blueprint('pedidos', __name__)

# @pedido_bp.route('/pedidos', methods=['POST'])
# def criar_pedido():
#     pedido_data = request.json
#     _data_compra = datetime.strptime(pedido_data['data_compra'], '%Y-%m-%d').date()
#     novo_pedido = Pedido(data_compra=_data_compra, cliente_id=pedido_data['cliente_id'])
#     db.session.add(novo_pedido)
#     db.session.commit()
#     return jsonify({'id': novo_pedido.pedido_id, 'data_compra': novo_pedido.data_compra, 'cliente_id':novo_pedido.cliente_id, 'cliente_nome': novo_pedido.cliente.nome}), 
@pedido_bp.route('/pedidos', methods=['POST'])
def criar_pedido():
    pedido_data = request.json
    _data_compra = datetime.strptime(pedido_data['data_compra'], '%Y-%m-%d').date()
    
    # Verifica se o cliente existe no banco de dados
    cliente = Cliente.query.get(pedido_data['cliente_id'])
    if not cliente:
        return jsonify({'Mensagem': 'Cliente não encontrado'}), 404
    
    # Cria o pedido com o cliente existente
    novo_pedido = Pedido(data_compra=_data_compra, cliente_id=pedido_data['cliente_id'])
    db.session.add(novo_pedido)
    db.session.commit()

    return jsonify({
        'id': novo_pedido.pedido_id,
        'data_compra': novo_pedido.data_compra,
        'cliente_id': novo_pedido.cliente_id,
        'cliente_nome': cliente.cliente_nome
    })

@pedido_bp.route('/pedidos', methods=['GET'])
def listar_pedidos():
    pedidos = Pedido.query.all()
    lista_pedidos = []

    for p in pedidos:
        # Supondo que você tenha um relacionamento entre Pedido e Cliente
        cliente = Cliente.query.get(p.cliente_id)  # Acessa o cliente associado ao pedido

        # Supondo que você tenha um relacionamento entre Pedido e DetalhePedido
        detalhes = DetalhePedido.query.filter_by(dp_pedido_id=p.pedido_id).all()
        detalhes_lista = [
            {
                'produto_id': d.dp_produto_id,
                'quantidade': d.dp_quantidade,
                'preco': d.dp_preco,
                'desconto': d.dp_desconto
            }
            for d in detalhes
        ]

        lista_pedidos.append({
            'ID': p.pedido_id,
            'Data de Compra': p.data_compra,
            'Cliente ID': p.cliente_id,
            'Cliente Nome': cliente.cliente_nome if cliente else 'Cliente não encontrado',
            'Detalhes': detalhes_lista
        })

    return jsonify(lista_pedidos), 200

# @pedido_bp.route('/pedidos/<int:id>', methods=['PUT'])
# def atualizar_pedido(id):
#     dados = request.json
#     pedido = pedido.query.get(id)

#     if not pedido:
#         return jsonify({'Mensagem': 'Pedido não encontrado'}), 404

#     pedido.pedido_nome = dados['pedido_nome']
#     db.session.commit()

#     return jsonify({'Pedido alterado': pedido.pedido_nome})

@pedido_bp.route('/pedidos/<int:id>', methods=['PUT'])
def atualizar_pedido(id):
    dados = request.json
    pedido = Pedido.query.get(id)

    if not pedido:
        return jsonify({'Mensagem': 'Pedido não encontrado'}), 404

    # Atualiza informações do pedido, se fornecido
    if 'pedido_nome' in dados:
        pedido.pedido_nome = dados['pedido_nome']

    # Atualiza detalhes do pedido (produtos)
    if 'detalhes' in dados:
        for detalhe in dados['detalhes']:
            if 'dp_id' not in detalhe:
                return jsonify({'Mensagem': 'dp_id é necessário para atualizar o detalhe do pedido.'}), 400
            
            # Acha o detalhe pelo ID
            detalhe_pedido = DetalhePedido.query.get(detalhe['dp_id'])
            if detalhe_pedido:
                # Atualiza os campos conforme necessário
                detalhe_pedido.dp_quantidade = detalhe.get('dp_quantidade', detalhe_pedido.dp_quantidade)
                detalhe_pedido.dp_preco = detalhe.get('dp_preco', detalhe_pedido.dp_preco)
                detalhe_pedido.dp_desconto = detalhe.get('dp_desconto', detalhe_pedido.dp_desconto)
            else:
                return jsonify({'Mensagem': f'Detalhe do pedido com ID {detalhe["dp_id"]} não encontrado.'}), 404

    db.session.commit()

    return jsonify({'Mensagem': 'Pedido atualizado com sucesso', 'Pedido ID': pedido.pedido_id}), 200


# @produto_bp.route('/produtos/<int:id>', methods=['DELETE'])
# def excluir_produto(id):
#     #dados = request.json
#     produto = Produto.query.get(id)

#     if not produto:
#         return jsonify({'Mensagem': 'Produto não encontrado'})
    
#     db.session.delete(produto)
#     db.session.commit()

#     return jsonify({'Produto excluido'}), 200
@pedido_bp.route('/pedidos/<int:id>', methods=['DELETE'])
def excluir_produto(id):
    pedido_a_excluir = Pedido.query.get(id)  # Renomeie a variável

    if not pedido_a_excluir:
        return jsonify({'Mensagem': 'Produto não encontrado'}), 404  # Retorna 404 se o produto não for encontrado

    db.session.delete(pedido_a_excluir)
    db.session.commit()

    return jsonify({'Mensagem': 'Produto excluído com sucesso'}), 200  # Retorna a mensagem de sucesso
