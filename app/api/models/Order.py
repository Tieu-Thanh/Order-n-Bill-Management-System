from . import db
from .OrderItem import OrderItem
from .Bill import Bill

class Order:
    def __init__(self, order_id, total_price, bill_id, status="pending"):
        self.order_id = order_id
        self.total_price = total_price
        self.status = status
        self.bill_id = bill_id
        # self.ordered_items = ordered_items if ordered_items else []

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "total_price": self.total_price,
            "bill_id": self.bill_id,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["order_id"],
            data["total_price"],
            data["bill_id"],
            data["status"]
        )

    def save(self):
        order_ref = db.collection('orders').document(self.order_id)
        order_ref.set(self.to_dict())

    def update_status(self, new_status):
        order_ref = db.collection("orders").document(self.order_id)

        if not order_ref.get().exists:
            return {'message': 'Order not found'}, 404

        order_ref.update({
            'status': new_status
        })

    @classmethod
    def get_ordered_items(cls, order_id):
        order_items_ref = db.collection('orders').document(order_id).collection('order_items')
        order_items = order_items_ref.stream()
        return [OrderItem.from_dict(item.to_dict()) for item in order_items]

    @classmethod
    def get_orders(cls):
        order_ref = db.collection('orders')
        orders = order_ref.stream()
        return [cls.from_dict(order.to_dict()) for order in orders]

    @classmethod
    def get_order_by_id(cls, order_id):
        order_ref = db.collection('orders')
        doc_ref = order_ref.document(order_id).get()

        if not doc_ref.exists:
            return None

        order = cls.from_dict(doc_ref.to_dict())

        return order

    def delete(self):
        db.collection('orders').document(self.order_id).delete()

    def get_bill(self):
        return Bill.get_bill_by_id(self.bill_id)
