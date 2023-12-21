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
    def __init__(self, item_id, name, description, price, is_on_stock=True, category=None, image_url=None):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.price = price
        self.is_on_stock = is_on_stock
        self.category = category
        self.image_url = image_url

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "is_on_stock": self.is_on_stock,
            "category": self.category,
            "image_url": self.image_url
        }

    @classmethod
    def save(cls, menu_item):
        menu_ref = db.collection('menu_items')
        query = menu_ref.where('item_id', '==', menu_item.item_id).limit(1).get()
        if any(query):
            return {'error:' f"Item with id {menu_item.item_id} already exists"}, 400
        doc_ref = menu_ref.document(menu_item.item_id).set(menu_item.to_dict())
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
            menu_item.item_id = doc_ref.id
            return menu_item
        else:
            return None

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        menu_ref = db.collection('menu_items')
        menu_ref.document(self.item_id).update(self.to_dict())

    def delete(self):
        menu_ref = db.collection('menu_items')
        menu_ref.document(self.item_id).delete()

    @classmethod
    def from_firestore_data(cls, data):
        return cls(
            item_id=data.get('item_id'),
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            is_on_stock=data.get('is_on_stock'),
            category=data.get('category'),
            image_url=data.get('image_url')
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


class OrderItem:
    def __init__(self, menu_item_id, quantity, special_request, status="pending", amount=None):
        self.menu_item_id = menu_item_id
        self.quantity = quantity
        self.special_request = special_request
        self.status = status
        self.amount = self.calculate_total()

    def calculate_total(self):
        menu_doc = db.collection('menu_items').document(self.menu_item_id).get()
        menu_item_price = menu_doc.to_dict()['price']
        self.amount = menu_item_price * self.quantity
        return self.amount

    def to_dict(self):
        self.calculate_total()  # update amount before serialization.
        return {
            'menu_item_id': self.menu_item_id,
            'quantity': self.quantity,
            'special_request': self.special_request,
            'amount': self.amount,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            menu_item_id=data.get('menu_item_id'),
            quantity=data.get('quantity'),
            special_request=data.get('special_request'),
            status=data.get('status'),
            amount=data.get('amount')
        )


class Order:
    def __init__(self, order_id, total_price, status="pending"):
        self.order_id = order_id
        self.total_price = total_price
        self.status = status

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "total_price": self.total_price,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
                data["order_id"],
                data["total_price"],
                data["status"]
            )

    def update_status(self, new_status):
        self.status = new_status
        order_ref = db.collection("orders").document(self.order_id[0])

        order_ref.update({
            'status': self.status
        })

    # def calculate_total_price(self):
    #     total_price = 0.0
    #     for item in self.order_items:
    #         total_price += item.price
    #     return total_price

    def get_order_items(self):
        order_items_ref = db.collection('orders').document(self.order_id).collection('order_items')
        order_items = order_items_ref.stream()
        return [OrderItem.from_dict(item.to_dict()) for item in order_items]

    # def get_ordered_item_by_id(self, order_item_id):
    #     order_items_ref = db.collection('orders').document(self.order_id).collection('order_items')
    #     query = order_items_ref.where('menu_item_id', '==', order_item_id).limit(1).stream()
    #
    #     for item_doc in query:
    #         return OrderItem.from_dict(item_doc.to_dict())
    #
    #     return None

    @classmethod
    def get_orders(cls):
        order_ref = db.collection('orders')
        orders = order_ref.stream()
        return [cls.from_dict(order.to_dict()) for order in orders]

    @classmethod
    def get_detail_order(cls, order_id):
        order_ref = db.collection('orders')
        doc_ref = order_ref.document(order_id).get()

        if not doc_ref.exists:
            return None

        order = cls.from_dict(doc_ref.to_dict())
        order.id = doc_ref.id

        # Fetch order items
        order_items = order.get_order_items()

        # Assign order items to the order instance
        order.order_items = order_items

        return order

    def delete(self):
        order_ref = db.collection('orders').document(self.order_id).delete()


class Table:
    def __init__(self, table_number, capacity, status):
        self.table_number = table_number
        self.capacity = capacity
        self.status = status

    def to_dict(self):
        return {
            "table_number": self.table_number,
            "capacity": self.capacity,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["table_number"],
            data["capacity"],
            data["status"]
        )


class Bill:
    def __init__(self, order_id, diner_id, table_id, menu_items, total_price, payment_method, payment_status='Unpaid'):
        self.order_id = order_id
        self.diner_id = diner_id
        self.table_id = table_id
        self.menu_items = menu_items
        self.total_price = total_price
        self.payment_method = payment_method
        self.payment_status = payment_status

    def to_firestore_data(self):
        return {
            "order_id": self.order_id,
            "diner_id": self.diner_id,
            "table_id": self.table_id,
            "menu_items": self.menu_items,
            "total_price": self.total_price,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status
        }

    @classmethod
    def from_firestore_data(cls, data):
        return cls(
            data["order_id"],
            data["diner_id"],
            data["table_id"],
            data["menu_items"],
            data["total_price"],
            data["payment_method"],
            data["payment_status"]
        )
