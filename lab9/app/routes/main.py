from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')


@main_bp.route('/about')
def about():
    return jsonify({'message': 'This is an about page!'})



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
        new_user = User(username=data['username'], password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return render_template('login.html')

    return render_template('register.html')


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        if not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Username and password are required'}), 400

        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'message': 'Invalid username or password'}), 401

        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token})

    return render_template('login.html')


@main_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return render_template('profile.html', username=user.username, bonus_level=user.bonus_level)
