# from google.api_core.datetime_helpers import DatetimeWithNanoseconds

from . import db
from datetime import datetime
from google.cloud import firestore
# from google.cloud.firestore_v1.base_query import FieldFilter
# from .Order import Order

class Bill:
    # def __init__(self, bill_id, diner_id, table_id,
    #              shift="", payment_method="", payment_status="Unpaid",
    #              date=datetime.now().strftime("%d/%m/%Y, %H:%M:%S")):
    #     self.bill_id = bill_id
    #     self.diner_id = diner_id
    #     self.table_id = table_id
    #     self.shift = shift
    #     self.payment_method = payment_method
    #     self.payment_status = payment_status
    #     self.date = date
    #     self.order_ids = self.get_order_ids()
    #     self.total_price = 0
    def __init__(self, bill_id, diner_id, table_id, **kwargs):
        self._bill_id = bill_id
        self._diner_id = diner_id
        self._table_id = table_id
        self._shift = kwargs.get("shift", self.set_shift())
        self._payment_method = kwargs.get("payment_method", "")
        self._payment_status = kwargs.get("payment_status", "Unpaid")
        self._date = kwargs.get("date", datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
        self._order_ids = kwargs.get("order_ids", self.get_orders_by_bill_id())  # Initialize as an empty list
        self._total_price = 0  # Calculate on demand

    def to_dict(self):
        return {
            "bill_id": self._bill_id,
            "diner_id": self._diner_id,
            "table_id": self._table_id,
            "shift": self._shift,
            "total_price": self.calculate_total_price(),  # Calculate total price before saving
            "payment_method": self._payment_method,
            "payment_status": self._payment_status,
            "date": self._date,
            "order_ids": self._order_ids,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def save(self):
        bill_ref = db.collection('bills').document(self._bill_id)
        bill_ref.set(self.to_dict())

    def delete_from_db(self):
        bill_ref = db.collection('bills').document(self._bill_id)
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

    def get_orders_by_bill_id(self):
        """Retrieves order documents from Firestore based on the provided bill_id."""
        orders_ref = db.collection('orders').where('bill_id', '==', self._bill_id)
        orders_snapshot = orders_ref.stream()

        # orders = [doc.to_dict() for doc in orders_snapshot]
        # return orders
        detailed_orders = []
        for order_doc in orders_snapshot:
            order_data = order_doc.to_dict()

            # Fetch order items directly from the sub-collection
            order_items_ref = db.collection("orders").document(order_data["order_id"]).collection("order_items")
            order_items_snapshot = order_items_ref.stream()
            order_items = [item.to_dict() for item in order_items_snapshot]

            order_data["order_items"] = order_items  # Add fetched items to order data
            detailed_orders.append(order_data)
        return detailed_orders

    def update_status(self, payment_status, payment_method):
        self._payment_status = payment_status
        self._payment_method = payment_method

        # Field updates:
        data = {
            "payment_status": self._payment_status,
            "payment_method": self._payment_method
        }

        bill_ref = db.collection('bills').document(self.bill_id)
        bill_ref.update(data)

    def change_table(self, new_table_id):
        self._table_id = new_table_id
        bill_ref = db.collection('bills').document(self._bill_id)
        bill_ref.update({"table_id": self._table_id})

    def calculate_total_price(self):
        """Calculates the total price of the bill by summing the total_price of each associated order."""
        orders = self.get_orders_by_bill_id()  # Fetch orders using the provided method
        total_price = 0
        for order in orders:
            total_price += order.get("total_price", 0)  # Add total_price from each order
        return total_price

    def set_shift(self):
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 15:
            return "A"
        return "B"