from flask import Blueprint, request, jsonify
from models import db, Produto

# instância(objeto) de Blueprint
produto_bp = Blueprint('produtos', __name__)

# Decorator da rota produtos, que é do tipo POST (enviando dados)
@produto_bp.route('/produtos', methods=['POST'])
def criar_produto():
    
    produto = request.json
    novo_produto = Produto(produto_nome=produto['produto_nome'],                           produto_preco=produto['produto_preco'])
    db.session.add(novo_produto)
    db.session.commit()
    
    return jsonify({'id': novo_produto.produto_id, 'nome': novo_produto.produto_nome, 'preco': novo_produto.produto_preco}), 201


@produto_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()

    return jsonify([{'ID': p.produto_id, 'Nome': p.produto_nome, 'preco': p.produto_preco} for p in produtos]), 200 

@produto_bp.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    dados = request.json
    produto = Produto.query.get(id)

    if not produto:
        return jsonify({'Mensagem': 'Produto não encontrado'}), 404

    produto.produto_nome = dados['produto_nome']
    db.session.commit()

    return jsonify({'Produto alterado': produto.produto_nome})

@produto_bp.route('/produtos/<int:id>', methods=['DELETE'])
def excluir_produto(id):
    #dados = request.json
    produto = Produto.query.get(id)

    if not produto:
        return jsonify({'Mensagem': 'Produto não encontrado'})
    
    db.session.delete(produto)
    db.session.commit()

    return jsonify({'Mensagem': 'Produto excluído'}), 200