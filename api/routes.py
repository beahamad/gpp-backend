from app import db
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from email_sender import send_email
from models import User, Phone
from flask_cors import cross_origin

user_routes = Blueprint('user_routes', __name__)
@user_routes.route('/register/phone', methods=['POST'])
@jwt_required()
@cross_origin()
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
        return jsonify({'error': 'IMEI é um campo obrigatório'}), 400

    # Check if phone IMEI is already registered
    if Phone.query.filter_by(imei=imei).first():
        return jsonify({'error': 'IMEI já registrado'}), 400

    # Create new phone for the user
    phone = Phone(imei=imei, number1=number1, number2=number2, user=current_user, model=model)
    db.session.add(phone)
    db.session.commit()

    return jsonify({'message': 'Aparelho registrado com sucesso!'}), 201

@user_routes.route('/remove/phone', methods=['POST'])
@jwt_required()
@cross_origin()
def remove_phone():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    data = request.get_json()

    # Extract phone IMEI from request
    imei = data.get('imei')

    # Find phone by IMEI and associated with the current user
    phone = Phone.query.filter_by(imei=imei, user=current_user).first()

    if not phone:
        return jsonify({'error': 'Aparelho não encontrado'}), 404

    db.session.delete(phone)
    db.session.commit()

    return jsonify({'message': 'Aparelho removido com sucesso'}), 200

@user_routes.route('/profile', methods=['GET'])
@jwt_required()
@cross_origin()
def get_profile():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)


    phones = current_user.phones

    phonesLost = []

    for phone in phones:
        if phone.is_lost:
            phonesLost.append(phone)


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
        } for phone in phones],
        'lostPhones': [{
            'imei': phone.imei,
            'number1': phone.number1,
            'number2': phone.number2,
            'is_lost': phone.is_lost,
            'model': phone.model
        }for phone in phonesLost],
        'isPolicia': current_user.ispolicia
    }

    return jsonify(profile_data), 200

@user_routes.route('/phone/losts', methods=['GET'])
@jwt_required()
@cross_origin()
def get_lost_phones():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user.ispolicia:
        return jsonify({'error': 'Usuario não é policial'}), 401

    phones = Phone.query.filter_by(is_lost = True).all()
    phone_list = []

    for phone in phones:
        phone_data = {
            'imei': phone.imei,
            'number1': phone.number1,
            'number2': phone.number2,
            'model': phone.model
        } 
        phone_list.append(phone_data)



    return jsonify(phone_list), 200

@user_routes.route('/phone/founds', methods=['GET'])
@jwt_required()
@cross_origin()
def get_found_phones():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user.ispolicia:
        return jsonify({'error': 'Usuario não é policial'}), 401

    phones = Phone.query.filter_by(is_found = True).all()
    phone_list = []

    for phone in phones:
        phone_data = {
            'imei': phone.imei,
            'number1': phone.number1,
            'number2': phone.number2,
            'model': phone.model
        } 
        phone_list.append(phone_data)



    return jsonify(phone_list), 200


@user_routes.route('/profile', methods=['PUT'])
@jwt_required()
@cross_origin()
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

    return jsonify({'message': 'Perfil atualizado com sucesso'}), 200

@user_routes.route('/phone/lost', methods=['POST'])
@cross_origin()
@jwt_required()
def mark_phone_as_lost():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    data = request.get_json()

    # Extract phone IMEI
    imei = data.get('imei')
    boletim = data.get('boletim')

    # Find phone by IMEI and associated with the current user
    phone = Phone.query.filter_by(imei=imei, user=current_user).first()

    if not phone:
        return jsonify({'error': 'Aparelho não encontrado'}), 404

    # Mark phone as lost
    phone.is_lost = True
    phone.boletim = boletim
    db.session.commit()

    msg = ""
    if boletim:
        msg = "Aparelho marcado como perdido e o BO foi registrado"
    else:
        msg = "Aparelho marcado como perdido e nenhum BO foi registrado"

    return jsonify({'message': msg}), 200

@user_routes.route('/phone/report', methods=['POST'])
@cross_origin()
@jwt_required()
def register_boletim():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    data = request.get_json()

    # Extract phone IMEI
    imei = data.get('imei')

    # Find phone by IMEI and associated with the current user
    phone = Phone.query.filter_by(imei=imei, user=current_user).first()

    if not phone:
        return jsonify({'error': 'Aparelho não encontrado'}), 404

    # Mark phone as lost
    phone.boletim = True
    db.session.commit()

    msg = "Boletim de ocorrência foi registrado com sucesso!"

    return jsonify({'message': msg}), 200


@user_routes.route('/phone/delicti', methods=['POST'])
@jwt_required()
@cross_origin()
def solicit_corpus_delicti():
    data = request.get_json()

    # Get the current user address
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)


    if not current_user.ispolicia:
        return jsonify({'error': 'Usuario não é policial'}), 401
    

    address = current_user.address

    # Extract IMEI
    imei = data.get('imei')

    # Find phone number by IMEI
    phone_number = Phone.query.filter_by(imei=imei).first()

    if not phone_number:
        return jsonify({'error': 'Aparelho não encontrado'}), 404
    
    if not phone_number.boletim:
        return jsonify({'error': 'Boletim de ocorrência não registrado nesse aparelho'}), 404
    

    # Retrieve owner's contact information
    owner = phone_number.user
    owner_contact = {
        'full_name': owner.full_name,
        'email': owner.email
    }

    recipient_email = owner_contact['email']
    subject = 'GPP - Sua presença foi solicitada'
    message = f'Olá, {owner_contact["full_name"]}.\n\nSua presença foi solicitada para realização do procedimento de corpo de delito com relação à perda do ceu celular com o imei {imei}, reportado no boletim de ocorrencia.\Por favor, compareça à delegacia no endereço {address} assim que possível.'

    try:
        send_email(recipient_email, subject, message)
        return jsonify({'owner_contact': owner_contact}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401


@user_routes.route('/phone/found', methods=['POST'])
@jwt_required()
@cross_origin()
def report_found_phone():
    data = request.get_json()

    # Get the current user address
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)


    if not current_user.ispolicia:
        return jsonify({'error': 'Usuario não é policial'}), 401
    

    address = current_user.address

    # Extract IMEI
    imei = data.get('imei')

    # Find phone number by IMEI
    phone_number = Phone.query.filter_by(imei=imei).first()

    if not phone_number:
        return jsonify({'error': 'Aparelho não encontrado'}), 404

    if phone_number.isfound:
        return jsonify({'error': 'Aparelho já foi marcado como encontrado'}), 404


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
        phone_number.is_found = True
        db.session.add(phone_number)
        db.session.commit()
        return jsonify({'owner_contact': owner_contact}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401
