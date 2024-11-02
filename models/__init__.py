from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .produto import db, Produto
from .cliente import db, Cliente
from .pedido import db, Pedido
from .usuario import db, Usuario
from .categoria import db, Categoria
