from . import db 

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    desconto = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Pedido {self.id}>'