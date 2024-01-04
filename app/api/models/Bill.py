from google.api_core.datetime_helpers import DatetimeWithNanoseconds

from . import db
from datetime import datetime
from google.cloud import firestore


class Bill:
    def __init__(self, bill_id, order_ids, diner_id, table_id,
                 payment_method, total_price, payment_status, shift):
        self.bill_id = bill_id
        self.order_ids = order_ids
        self.diner_id = diner_id
        self.table_id = table_id
        self.shift = shift
        self.total_price = total_price
        self.payment_method = payment_method
        self.payment_status = payment_status

    def to_dict(self):
        return {
            "bill_id": self.bill_id,
            "order_ids": self.order_ids,
            "diner_id": self.diner_id,
            "table_id": self.table_id,
            "shift": self.shift,
            "total_price": self.total_price,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status
        }

    def str_time(self):
        return str(self.shift)

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["bill_id"],
            data["order_ids"],
            data["diner_id"],
            data["table_id"],
            data["total_price"],
            data["payment_method"],
            data["payment_status"],
            data["shift"].strftime("%m/%d/%Y %H:%M:%S")
        )

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

    def save(self):
        bill_ref = db.collection('bills').document(self.bill_id)
        bill_ref.set(self.to_dict())

    def update_status(self, status):
        self.payment_status = status
        self.save()

    def delete_from_db(self):
        bill_ref = db.collection('bills').document(self.bill_id)
        bill_ref.delete()

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


