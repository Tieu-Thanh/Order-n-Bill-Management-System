from . import db
from .OrderItem import OrderItem


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
