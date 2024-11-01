from .import db
from sqlalchemy import Column, Integer, String


class Cliente(db.Model):
  
    __tablename__ = 'clientes'

    cliente_id = db.Column(db.Integer, primary_key=True)
    cliente_nome = db.Column(db.String(50))
    cliente_email = db.Column(db.String(50))

