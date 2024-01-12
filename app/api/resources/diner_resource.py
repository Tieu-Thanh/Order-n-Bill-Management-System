# api/resources/diner_resource.py
from flask_restful import Resource, reqparse
from firebase_admin import firestore
from app.api.models.Diner import Diner


class DinerResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('phone_number', type=str)
        self.parser.add_argument('gender', type=str)
        self.parser.add_argument('birthday', type=str)

    def post(self):
        args = self.parser.parse_args()

        # try:
        phone_number = args['phone_number']
        existing_diner = Diner.get_diner_by_phone_number(phone_number)
        if existing_diner:
            return {'error': 'Diner with the given phone number already exists'}, 400

        new_diner = Diner(**args)  # Use dictionary unpacking
        new_diner.create_diner()
        return {'message': 'Diner registration successful'}, 201

        # except Exception as e:
        #     return {'error': str(e)}, 400
