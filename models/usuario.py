from . import db

class Usuario(db.Model):

    __tablename__ = 'usuarios'

    usuario_id = db.Column(db.Integer, primary_key=True)
    usuario_login = db.Column(db.String(20), nullable=False, unique=True)
    usuario_senha = db.Column(db.String(20), nullable=False)
    