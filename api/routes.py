from app import db
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from email_sender import send_email
from models import User, Phone

user_routes = Blueprint('user_routes', __name__)
@user_routes.route('/register/phone', methods=['POST'])
@jwt_required()
def register_phone():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    data = request.get_json()

    # Extract phone data from request
    imei = data.get('imei')
    number1 = data.get('number1')
    number2 = data.get('number2')
    model = data.get('model')

    # Check if phone IMEI is valid
    if not imei:
        return jsonify({'error': 'IMEI is required'}), 400

    # Check if phone IMEI is already registered
    if Phone.query.filter_by(imei=imei).first():
        return jsonify({'error': 'IMEI already registered'}), 400

    # Create new phone for the user
    phone = Phone(imei=imei, number1=number1, number2=number2, user=current_user, model=model)
    db.session.add(phone)
    db.session.commit()

    return jsonify({'message': 'Phone registered successfully'}), 201

@user_routes.route('/remove/phone', methods=['POST'])
@jwt_required()
def remove_phone():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    data = request.get_json()

    # Extract phone IMEI from request
    imei = data.get('imei')

    # Find phone by IMEI and associated with the current user
    phone = Phone.query.filter_by(imei=imei, user=current_user).first()

    if not phone:
        return jsonify({'error': 'Phone not found'}), 404

    db.session.delete(phone)
    db.session.commit()

    return jsonify({'message': 'Phone removed successfully'}), 200

@user_routes.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    profile_data = {
        'cpf': current_user.cpf,
        'full_name': current_user.full_name,
        'date_of_birth': current_user.date_of_birth.isoformat(),
        'address': current_user.address,
        'email': current_user.email,
        'phones': [{
            'imei': phone.imei,
            'number1': phone.number1,
            'number2': phone.number2,
            'is_lost': phone.is_lost,
            'model': phone.model
        } for phone in current_user.phones]
    }

    return jsonify(profile_data), 200

@user_routes.route('/profile', methods=['PUT'])
@jwt_required()
def edit_profile():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    data = request.get_json()

    # Extract data to be updated
    full_name = data.get('full_name')
    address = data.get('address')
    password = data.get('password')

    # Update user data
    if full_name:
        current_user.full_name = full_name
    if address:
        current_user.address = address
    if password:
        current_user.password = password

    db.session.commit()

    return jsonify({'message': 'Profile updated successfully'}), 200

@user_routes.route('/phone/lost', methods=['POST'])
@jwt_required()
def mark_phone_as_lost():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    data = request.get_json()

    # Extract phone IMEI
    imei = data.get('imei')

    # Find phone by IMEI and associated with the current user
    phone = Phone.query.filter_by(imei=imei, user=current_user).first()

    if not phone:
        return jsonify({'error': 'Phone not found'}), 404

    # Mark phone as lost
    phone.is_lost = True
    db.session.commit()

    return jsonify({'message': 'Phone marked as lost'}), 200

@user_routes.route('/phone/found', methods=['POST'])
@jwt_required()
def report_found_phone():
    data = request.get_json()

    # Get the current user address
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    address = current_user.address

    # Extract IMEI
    imei = data.get('imei')

    # Find phone number by IMEI
    phone_number = Phone.query.filter_by(imei=imei).first()

    if not phone_number:
        return jsonify({'error': 'Phone number not found'}), 404

    # Retrieve owner's contact information
    owner = phone_number.user
    owner_contact = {
        'full_name': owner.full_name,
        'email': owner.email
    }

    recipient_email = owner_contact['email']
    subject = 'GPP - Seu telefone foi encontrado!'
    message = f'Olá, {owner_contact["full_name"]}.\n\nSeu telefone com o IMEI {imei} foi encontrado!\nProcure a delegacia no endereço {address}.'

    try:
        send_email(recipient_email, subject, message)
        return jsonify({'owner_contact': owner_contact}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401
