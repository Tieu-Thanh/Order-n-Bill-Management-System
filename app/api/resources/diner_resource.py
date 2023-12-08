# api/resources/diner_resource.py
from flask_restful import Resource, reqparse
from firebase_admin import firestore
from app.models import Diner


class DinerResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('phone_number', type=str, required=True)
        parser.add_argument('gender', type=str, required=True)
        parser.add_argument('birthday', type=str, required=True)
        args = parser.parse_args()

        name = args['name']
        phone_number = args['phone_number']
        gender = args['gender']
        birthday = args['birthday']

        try:
            # Check if the phone number already exists
            db = firestore.client()
            existing_diner_ref = db.collection('diners').where('phone_number', '==', phone_number).limit(1).get()

            if existing_diner_ref:
                return {'error': 'Diner with the given phone number already exists'}, 400

            # Create a new diner instance
            new_diner = Diner(
                name=name,
                phone_number=phone_number,
                gender=gender,
                birthday=birthday
            )

            # Add the diner data to the 'diners' collection in Firestore
            diner_ref = db.collection('diners').add(new_diner.to_dict())

            # Return diner information
            return {'message': 'Diner registration successful'}, 201
        except Exception as e:
            return {'error': str(e)}, 400
