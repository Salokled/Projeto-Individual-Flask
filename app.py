from flask import Flask
from models import db
from config import Config
from controllers import produto_bp, pedido_bp, usuario_bp, cliente_bp, login_bp, categoria_bp
from flask_jwt_extended import JWTManager

def criar_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    #generate random secret key long
    app.config['JWT_SECRET_KEY'] = 'ASE$@$$ASEASDUASDA'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400 # o token expira em 24h
    db.init_app(app)
    jwt = JWTManager(app)
    
    with app.app_context():
        db.create_all()

    for bp in [produto_bp, pedido_bp, usuario_bp, cliente_bp, login_bp, categoria_bp]:	
        app.register_blueprint(bp)

    @app.route('/')
    def index():
        return '<h1>Testes de CRUD</h1><br>'
    return app

if __name__ == '__main__':
    app = criar_app()
    app.run(debug=True)