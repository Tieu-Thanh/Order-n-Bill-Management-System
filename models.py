# models.py
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore


# Initialize Firebase Admin SDK
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


class MenuItem:
    def __init__(self, name, description, price, is_on_stock=True, category=None):
        self.name = name
        self.description = description
        self.price = price
        self.is_on_stock = is_on_stock
        self.category = category

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "isOnStock": self.is_on_stock,
            "category": self.category
        }

    @classmethod
    def save(cls, menu_item):
        menu_ref = db.collection('menu_items')
        doc_ref = menu_ref.add(menu_item.to_dict())

        return menu_item

    @classmethod
    def list_items(cls):
        menu_ref = db.collection('menu_items')
        menu_items = menu_ref.stream()
        return [cls.from_firestore_data(menu_item) for menu_item in menu_items]

    @classmethod
    def from_firestore_data(cls, data):
        return cls(
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            is_on_stock=data.get('isOnStock', True),
            category=data.get('category')
        )