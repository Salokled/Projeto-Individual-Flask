from flask import Blueprint, request, jsonify
from models import db, Cliente
from flask_jwt_extended import jwt_required


cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/cliente', methods=['POST'])
@jwt_required()
def criar_cliente():
    dados = request.json
    if not all(key in dados for key in ('nome', 'cpf', 'email', 'telefone')):
        return jsonify({'erro': 'Faltam dados'}), 400
    novo_cliente = Cliente(nome=dados['nome'], cpf=dados['cpf'], email=dados['email'], telefone=dados['telefone'])
    db.session.add(novo_cliente)
    db.session.commit()
    return jsonify({'id': novo_cliente.id, 'nome': novo_cliente.nome, 'cpf': novo_cliente.cpf, 'email': novo_cliente.email, 'telefone': novo_cliente.telefone}), 201

@cliente_bp.route('/cliente', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    if not clientes:
        return jsonify({'erro': 'Nenhum cliente encontrado'}), 404
    return jsonify([{'id': c.id, 'nome': c.nome, 'cpf': c.cpf, 'email': c.email, 'telefone': c.telefone} for c in clientes]), 200

@cliente_bp.route('/cliente/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    dados = request.json
    if not any(key in dados for key in ('nome', 'cpf', 'email', 'telefone')):
        return jsonify({'erro': 'Nenhum dado foi alterado'}), 400
    
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404

    cliente.nome = dados.get('nome', cliente.nome)
    cliente.cpf = dados.get('cpf', cliente.cpf)
    cliente.email = dados.get('email', cliente.email)
    cliente.telefone = dados.get('telefone', cliente.telefone)
    db.session.commit()
    return jsonify({'id': cliente.id, 'nome': cliente.nome, 'cpf': cliente.cpf, 'email': cliente.email, 'telefone': cliente.telefone}), 200

@cliente_bp.route('/cliente/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    cliente = Cliente.query.get(id)
    
    if not cliente:
        return jsonify({'erro': 'Cliente não encontrado'}), 404
    
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'mensagem': 'Cliente deletado com sucesso'}), 200