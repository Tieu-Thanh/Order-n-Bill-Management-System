# models.py
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('path/to/your/firebase/credentials.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def save(self):
        menu_ref = db.collection('menu_items')
        menu_ref.add({
            'name': self.name,
            'price': self.price
        })

    @classmethod
    def get_all(cls):
        menu_ref = db.collection('menu_items')
        return menu_ref.stream()


class Table:
    def __init__(self, number, capacity):
        self.number = number
        self.capacity = capacity

    def save(self):
        table_ref = db.collection('tables')
        table_ref.add({
            'number': self.number,
            'capacity': self.capacity
        })

    @classmethod
    def get_all(cls):
        table_ref = db.collection('tables')
        return table_ref.stream()


class Order:
    def __init__(self, table_number, items, status='pending'):
        self.table_number = table_number
        self.items = items
        self.status = status
        self.created_at = datetime.now()

    def save(self):
        order_ref = db.collection('orders')
        order_ref.add({
            'table_number': self.table_number,
            'items': self.items,
            'status': self.status,
            'created_at': self.created_at
        })

    @classmethod
    def get_all(cls):
        order_ref = db.collection('orders')
        return order_ref.stream()


class Chef:
    def __init__(self, name):
        self.name = name

    def save(self):
        chef_ref = db.collection('chefs')
        chef_ref.add({
            'name': self.name
        })

    @classmethod
    def get_all(cls):
        chef_ref = db.collection('chefs')
        return chef_ref.stream()


class Staff:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def save(self):
        staff_ref = db.collection('staff')
        staff_ref.add({
            'name': self.name,
            'role': self.role
        })

    @classmethod
    def get_all(cls):
        staff_ref = db.collection('staff')
        return staff_ref.stream()


class Bill:
    def __init__(self, order_id, total_amount, status='unpaid'):
        self.order_id = order_id
        self.total_amount = total_amount
        self.status = status
        self.created_at = datetime.now()

    def save(self):
        bill_ref = db.collection('bills')
        bill_ref.add({
            'order_id': self.order_id,
            'total_amount': self.total_amount,
            'status': self.status,
            'created_at': self.created_at
        })

    @classmethod
    def get_all(cls):
        bill_ref = db.collection('bills')
        return bill_ref.stream()
