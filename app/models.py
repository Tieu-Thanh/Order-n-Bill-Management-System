# models.py
import hashlib
import uuid
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from flask import current_app
from config import app_config

db = app_config.FIRESTORE


class MenuItem:
    def __init__(self, name, description, price, is_on_stock=True, category=None):
        self.name = name
        self.description = description
        self.price = price
        self.is_on_stock = is_on_stock
        self.category = category,
        self.id = None

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "is_on_stock": self.is_on_stock,
            "category": self.category
        }

    @classmethod
    def save(cls, menu_item):
        menu_ref = current_app.config['FIRESTORE'].collection('menu_items')
        doc_ref = menu_ref.add(menu_item.to_dict())
        menu_item.id = doc_ref[1].id  # retrieve ID from firestore
        return menu_item

    @classmethod
    def list_items(cls):
        menu_ref = db.collection('menu_items')
        menu_items = menu_ref.stream()
        return [cls.from_firestore_data(menu_item) for menu_item in menu_items]

    @classmethod
    def get_item(cls, menu_item_id):
        menu_ref = db.collection('menu_items')
        doc_ref = menu_ref.document(menu_item_id).get()
        if doc_ref.exists:
            menu_item = cls.from_firestore_data(doc_ref.to_dict())
            menu_item.id = doc_ref.id
            return menu_item
        else:
            return None

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        menu_ref = db.collection('menu_items')
        menu_ref.document(self.id).update(self.to_dict())

    def delete(self):
        menu_ref = db.collection('menu_items')
        menu_ref.document(self.id).delete()

    @classmethod
    def from_firestore_data(cls, data):
        return cls(
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            is_on_stock=data.get('is_on_stock'),
            category=data.get('category')
        )

    @classmethod
    def get_items_by_category(cls, category):
        menu_ref = db.collection('menu_items')
        query = menu_ref.where('category', '==', category).stream()
        return [cls.from_firestore_data(menu_item.to_dict()) for menu_item in query]


class Diner:
    def __init__(self, name, gender, phone_number, birthday):
        self.name = name
        self.phone_number = phone_number
        self.gender = gender
        self.birthday = birthday
        # self.id = id or self._generate_id()

    def to_dict(self):
        return {
            'name': self.name,
            'phone_number': self.phone_number,
            'gender': self.gender,
            'birthday': self.birthday
        }
