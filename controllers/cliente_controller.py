from flask import Blueprint, request, jsonify
from models import db, Cliente

# instância(objeto) de Blueprint
cliente_bp = Blueprint('clientes', __name__)

# Decorator da rota produtos, que é do tipo POST (enviando dados)
@cliente_bp.route('/clientes', methods=['POST'])
def criar_cliente():
    
    cliente = request.json
    novo_cliente = Cliente(cliente_nome=cliente['cliente_nome'],
                           cliente_email=cliente['cliente_email'])
    db.session.add(novo_cliente)
    db.session.commit()
    
    return jsonify({'id': novo_cliente.cliente_id, 'nome': novo_cliente.cliente_nome, 'email': novo_cliente.cliente_email}), 201

@cliente_bp.route('/clientes', methods=['GET'])
def listarClientes():
    clientes = Cliente.query.all()
    
    return jsonify([{'ID': c.cliente_id, 'Nome': c.cliente_nome, 'Email':c.cliente_email} for c in clientes]), 200

# Decorator da rota clientes, que é do tipo PUT (atualizando dados)
@cliente_bp.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    dados = request.json
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'Mensagem': 'Cliente não encontrado'}), 404
    cliente.cliente_nome = dados['cliente_nome']
    cliente.cliente_email = dados['cliente_email']
    db.session.commit()
    return jsonify({'Cliente alterado': cliente.cliente_nome})

@cliente_bp.route('/clientes/<int:id>', methods=['DELETE'])
def excluir_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'Mensagem': 'Cliente não encontrado'})
    
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'Mensagem': 'Cliente excluído'}), 200