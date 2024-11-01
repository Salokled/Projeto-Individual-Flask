from flask_sqlalchemy import SQLAlchemy

# Cria a instância do SQLAlchemy
db = SQLAlchemy()

# Importa os modelos (Produto e Usuario) após a criação do db
from .produto import Produto
from .usuario import Usuario
from .cliente import Cliente
from .pedido import Pedido
from .detalhe_pedido import DetalhePedido
