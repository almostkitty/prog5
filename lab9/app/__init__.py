from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config.from_object('config.Config')
    
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
