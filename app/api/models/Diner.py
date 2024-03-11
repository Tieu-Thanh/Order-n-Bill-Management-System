from . import db

import uuid
from datetime import datetime
from firebase_admin import firestore


class Diner:
    def __init__(self, name, gender, phone_number, birthday, **kwargs):
        self.id = str(uuid.uuid4())
        self.name = name
        self.phone_number = phone_number
        self.gender = gender
        self.birthday = birthday
        self.created_at = kwargs.get("created_at", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
        self.updated_at = kwargs.get("updated_at", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number,
            'gender': self.gender,
            'birthday': self.birthday,
            'created_at': self.created_at,  # Format for Firestore
            'updated_at': self.updated_at,  # Format for Firestore
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def create_diner(self):
        db.collection('diners').document(self.id).set(self.to_dict())

    @classmethod
    def get_diner_by_id(cls, diner_id):
        diner_ref = db.collection('diners').document(diner_id)
        diner_doc = diner_ref.get()
        if diner_doc.exists:
            return cls.from_dict(diner_doc.to_dict())
        return None

    @classmethod
    def get_diner_by_phone_number(cls, phone_number):
        existing_diner_docs = db.collection('diners').where('phone_number', '==', phone_number).get()
        if existing_diner_docs:
            # Access the first document if multiple exist
            existing_diner_doc = existing_diner_docs[0]
            return cls.from_dict(existing_diner_doc.to_dict())
        return None

    def update_diner(self):
        diner_ref = db.collection('diners').document(self.id)
        diner_ref.update(self.to_dict())

    def delete_diner(self):
        diner_ref = db.collection('diners').document(self.id)
        diner_ref.delete()


    # Add additional methods as needed (e.g., search by name, filter by criteria)


