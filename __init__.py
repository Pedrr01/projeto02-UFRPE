from flask import Flask
from app.routes.auth import auth_bp
from app.routes.usuarios import usuarios_bp
from app.routes.admin import admin_bp
from app.routes.disciplinas import disciplinas_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = '1110'

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(disciplinas_bp)

    return app
