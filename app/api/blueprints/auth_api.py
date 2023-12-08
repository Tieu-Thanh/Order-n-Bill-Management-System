from flask import Blueprint, request, jsonify
from firebase_admin import firestore

from app.models import Diner

auth_bp = Blueprint('auth', __name__)

db = firestore.client()


@auth_bp.route('/diners/register', methods=['POST'])
def register_diner():
    data = request.get_json()

    name = data.get('name')
    phone_number = data.get('phone_number')
    gender = data.get('gender')

    if not all([name, phone_number, gender]):
        return jsonify({'error': 'Incomplete request data. Ensure all required fields are provided.'}), 400

    try:
        existing_diner = db.collection(u'diners').where('phone_number', '==', phone_number).limit(1).get()
        if existing_diner:
            return jsonify({'error': 'Diner is existed with that phone number'}), 400

        new_diner = Diner(
            name=name,
            phone_number=phone_number,
            gender=gender)

        diner_ref = db.collection(u'diners').add(new_diner.to_dict())
        return jsonify({'message': 'Diner registration successful'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400
