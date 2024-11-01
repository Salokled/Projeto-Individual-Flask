from . import db

class Pedido(db.Model):
    __tablename__ = "pedidos"

    pedido_id = db.Column(db.Integer, primary_key=True)
    data_compra = db.Column(db.Date)

    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.cliente_id'), nullable=False) 

    cliente = db.relationship('Cliente', backref='pedidos', lazy='select')