from . import db 

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Produto {self.nome}>'