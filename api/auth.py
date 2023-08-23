import random
from email_sender import send_email
from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token
from app import db
from models import User
from utils import is_valid_email, is_valid_cpf
from flask_cors import cross_origin

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['POST'])
@cross_origin()
def register():
    data = request.get_json()

    # Extract user data from request
    cpf = data.get('cpf')
    full_name = data.get('full_name')
    date_of_birth = data.get('date_of_birth')
    address = data.get('address')
    email = data.get('email')
    password = data.get('password')

    # Check if CPF and email are valid
    if not is_valid_cpf(cpf):
        return jsonify({'error': 'Invalid CPF'}), 400
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email'}), 400

    # Check if CPF and email are already registered
    if User.query.filter_by(cpf=cpf).first():
        return jsonify({'error': 'CPF already registered'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    # Generate confirmation code
    confirmation_code = generate_confirmation_code()

    # Create new user
    user = User(cpf=cpf, full_name=full_name, date_of_birth=date_of_birth,
                address=address, email=email, password=password, confirmation_code=confirmation_code)
    db.session.add(user)
    db.session.commit()

    # Send confirmation email
    try:
        send_confirmation_email(email, confirmation_code)

    except Exception:
        return jsonify({'error': "Não foi possível enviar o email, tente novamente mais tarde"})

    return jsonify({'message': 'Código de confirmação enviado para seu email'}), 201

@auth_routes.route('/register/policia', methods=['POST'])
@cross_origin()
def register_policia():
    data = request.get_json()

    # Extract user data from request
    cpf = data.get('cpf')
    full_name = data.get('full_name')
    date_of_birth = data.get('date_of_birth')
    address = data.get('address')
    email = data.get('email')
    password = data.get('password')

    # Check if CPF and email are valid
    if not is_valid_cpf(cpf):
        return jsonify({'error': 'Invalid CPF'}), 400
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email'}), 400

    # Check if CPF and email are already registered
    if User.query.filter_by(cpf=cpf).first():
        return jsonify({'error': 'CPF already registered'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    # Generate confirmation code
    confirmation_code = generate_confirmation_code()

    # Create new user
    user = User(cpf=cpf, full_name=full_name, date_of_birth=date_of_birth,
                address=address, email=email, password=password, ispolicia=True, confirmed=True)
    db.session.add(user)
    db.session.commit()

    # Send confirmation email

    return jsonify({'message': 'Policial Registrado com sucesso'}), 201

@auth_routes.route('/confirm', methods=['POST'])
@cross_origin()
def confirm_registration():
    data = request.get_json()

    # Extract email and confirmation code from request
    email = data.get('email')
    confirmation_code = data.get('confirmation_code')

    # Find user by email and confirmation code
    user = User.query.filter_by(email=email, confirmation_code=confirmation_code).first()

    if not user:
        return jsonify({'error': 'Email ou codigo de confirmação inválidos'}), 401

    # Remove confirmation code and mark user as confirmed
    user.confirmation_code = None
    user.confirmed = True
    db.session.commit()

    # Generate access token
    access_token = create_access_token(identity=user.id)

    return jsonify({'access_token': access_token}), 200

def generate_confirmation_code():
    return str(random.randint(1000, 9999))

def send_confirmation_email(email, confirmation_code):
    subject = 'GPP - Código de Confirmação'
    message = f'Seu código de confirmação é: {confirmation_code}.'

    send_email(email, subject, message)
    return jsonify({'error': "Não foi possível enviar o email, tente novamente mais tarde"})
    
@auth_routes.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.get_json()

    # Extract email and password from request
    email = data.get('email')
    password = data.get('password')

    # Find user by email
    user = User.query.filter_by(email=email).first()


    # Check if user exists and password is correct
    if not user or user.password != password:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    if not user.confirmed:
        confirmation_code = user.confirmation_code
        try:
            send_confirmation_email(email, confirmation_code)

        except Exception:
            return jsonify({'error': "Não foi possível enviar o email, tente novamente mais tarde"})
        
        return jsonify({'error': 'Usuário não confirmado'}), 401
        
    # Generate access token
    access_token = create_access_token(identity=user.id)

    return jsonify({'access_token': access_token}), 200
