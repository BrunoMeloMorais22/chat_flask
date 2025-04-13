from db import db

class User(db.Model):

    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    novoUsername = db.Column(db.String(100), nullable=False, unique=True)
    novaSenha = db.Column(db.String(100), nullable=False)