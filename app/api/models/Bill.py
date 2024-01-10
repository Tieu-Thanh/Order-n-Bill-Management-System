# from google.api_core.datetime_helpers import DatetimeWithNanoseconds

from . import db
from datetime import datetime
from google.cloud import firestore
# from google.cloud.firestore_v1.base_query import FieldFilter
# from .Order import Order

class Bill:
    def __init__(self, bill_id, diner_id, table_id,
                 shift="", payment_method="", payment_status="Unpaid",
                 date=datetime.utcnow().strftime("%d/%m/%Y, %H:%M:%S")):
        self.bill_id = bill_id
        self.diner_id = diner_id
        self.table_id = table_id
        self.shift = shift
        self.payment_method = payment_method
        self.payment_status = payment_status
        self.date = date
        self.order_ids = self.get_order_ids()
        self.total_price = self.calculate_total_price()

    def to_dict(self):
        return {
            "bill_id": self.bill_id,
            "diner_id": self.diner_id,
            "table_id": self.table_id,
            "shift": self.shift,
            "total_price": self.total_price,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status,
            "date": self.date,
            "order_ids": self.order_ids
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["bill_id"],
            data["diner_id"],
            data["table_id"],
            data["shift"],
            data["payment_method"],
            data["payment_status"],
            data["date"]
        )

    def save(self):
        bill_ref = db.collection('bills').document(self.bill_id)
        bill_ref.set(self.to_dict())

    def delete_from_db(self):
        bill_ref = db.collection('bills').document(self.bill_id)
        bill_ref.delete()

    @classmethod
    def get_bills(cls):
        bill_ref = db.collection('bills')
        bills = bill_ref.stream()
        return [cls.from_dict(bill.to_dict()) for bill in bills]

    @classmethod
    def get_bill_by_id(cls, bill_id):
        bill_ref = db.collection('bills').document(bill_id)
        bill_data = bill_ref.get()
        if bill_data.exists:
            return cls.from_dict(bill_data.to_dict())
        return None

    @classmethod
    def filter_bills(cls, filter_param, sort_field=None, sort_order="asc"):
        """
        Filters and sorts bills from Firestore based on specified parameters.
        Supports multiple filtering conditions on different fields.

        Args:
            filter_param (dict): A dictionary of filtering conditions (field: value pairs).
            sort_field (str, optional): Field to sort by. Defaults to None.
            sort_order (str, optional): Sorting order ('asc' or 'desc'). Defaults to "asc".

        Returns:
            list: A list of filtered and sorted Bill objects.
        """

        bill_ref = db.collection('bills')

        # Apply multiple filtering conditions efficiently
        filtered_query = bill_ref
        for field, value in filter_param.items():
            filtered_query = filtered_query.where(field, '==', value)  # Use '==' for equality filtering

        # Apply sorting if requested
        if sort_field:
            direction = firestore.Query.ASCENDING if sort_order == "asc" else firestore.Query.DESCENDING
            filtered_query = filtered_query.order_by(sort_field, direction=direction)

        # Retrieve filtered and sorted bills
        filtered_bills = filtered_query.stream()
        return [cls.from_dict(bill.to_dict()) for bill in filtered_bills]

    def get_order_ids(self):
        """Retrieves order IDs associated with the bill from the "orders" collection."""
        orders_ref = db.collection('orders')
        orders_query = orders_ref.where('bill_id', '==', self.bill_id)
        order_doc = orders_query.stream()

        order_ids = [order.id for order in order_doc]

        return order_ids

    def update_status(self, payment_status, payment_method):
        self.payment_status = payment_status
        self.payment_method = payment_method

        # Field updates:
        data = {
            "payment_status": self.payment_status,
            "payment_method": self.payment_method
        }

        bill_ref = db.collection('bills').document(self.bill_id)
        bill_ref.update(data)

    def get_orders_data(self):
        """Retrieves and returns order data associated with the bill."""
        orders_ref = db.collection('orders')
        orders_snapshot = orders_ref.where('order_id', 'in', self.order_ids).stream()

        orders_data = []
        for order_doc in orders_snapshot:
            order_data = order_doc.to_dict()
            order_items_ref = order_doc.reference.collection('order_items')
            order_items_snapshot = order_items_ref.stream()

            order_items_data = [item_doc.to_dict() for item_doc in order_items_snapshot]
            order_data['order_items'] = order_items_data

            orders_data.append(order_data)
        return orders_data

    def change_table(self, new_table_id):
        self.table_id = new_table_id
        bill_ref = db.collection('bills').document(self.bill_id)
        bill_ref.update({"table_id": self.table_id})

    def calculate_total_price(self):
        orders_data = self.get_orders_data()
        return sum(
            item.get("amount", 0)  # Directly access amount, default to 0
            for order in orders_data
            for item in order.get("order_items", [])
        )
