from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
jwt = JWTManager()



def create_app():
    app = Flask(__name__)
    
    # Подключаем конфигурацию
    app.config.from_object('config.Config')
    
    db.init_app(app)
    jwt.init_app(app)


    # Регистрируем маршруты
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    
    return app