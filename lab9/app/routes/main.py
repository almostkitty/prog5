from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime


# Создание токенов
class TokenFactory:
    def __init__(self, expiration_time_minutes=30):
        self.expiration_time_minutes = expiration_time_minutes

    def create_token(self, user_id):
        expiration_time = datetime.timedelta(minutes=self.expiration_time_minutes)
        return create_access_token(identity=user_id, expires_delta=expiration_time)


# Наблюдатель для обновления уровня бонусов
class BonusObserver:
    def update(self, user_id, amount):
        user = User.query.get(user_id)
        if user:
            user.total_spent += amount
            self.update_bonus_level(user)

    def update_bonus_level(self, user):
        if user.total_spent > 10000:
            user.bonus_level = 'Platinum'
        elif user.total_spent > 5000:
            user.bonus_level = 'Gold'
        else:
            user.bonus_level = 'Silver'
        db.session.commit()

# Инициализация токенов
token_factory = TokenFactory(expiration_time_minutes=60)  # Ограничение для токена на 1 час
bonus_observer = BonusObserver()

main_bp = Blueprint('main', __name__)


# Главная страница
@main_bp.route('/')
def home():
    return render_template('home.html')

# Регистрация
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        if not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Username and password are required'}), 400

        user = User.query.filter_by(username=data['username']).first()
        if user:
            return jsonify({'message': 'User already exists'}), 400

        hashed_password = generate_password_hash(data['password'])
        new_user = User(username=data['username'], password=hashed_password, total_spent=0, bonus_level='Bronze')

        db.session.add(new_user)
        db.session.commit()

        return render_template('login.html')

    return render_template('register.html')

@main_bp.route('/login-page', methods=['GET'])
def login_page():
    return render_template('login.html')

# Вход в систему и созадние токена
@main_bp.route('/login', methods=['POST'])
def login():
    data = request.form  # Используем request.form для получения данных формы
    if not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401

    # Создание JWT токена через фабрику + выводим уровень
    token = token_factory.create_token(user.id)
    return jsonify({'access_token': token,
                    'bonus_level': user.bonus_level})


# Профиль пользователя (с проверкой токена)
@main_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return render_template('profile.html', username=user.username, bonus_level=user.bonus_level)


# Добавление транзакции для пользователя
@main_bp.route('/users/<int:id>/transactions', methods=['POST'])
@jwt_required()
def add_transaction(id):
    user_id = get_jwt_identity()
    if user_id != id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    if not data.get('amount'):
        return jsonify({'message': 'Amount is required'}), 400

    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    amount = data['amount']
    user.total_spent += amount
    db.session.commit()

    # Уведомление наблюдателя об изменении транзакции
    bonus_observer.update(user.id, amount)

    return jsonify({'message': 'Transaction added and bonus level updated'})
