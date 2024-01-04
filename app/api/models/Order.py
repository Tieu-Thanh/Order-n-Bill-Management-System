from . import db
from .OrderItem import OrderItem


class Order:
    def __init__(self, order_id, total_price, billID="",  status="pending"):
        self.order_id = order_id
        self.total_price = total_price
        self.status = status
        self.billID = billID

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

    @classmethod
    def update_status(cls, order_id, new_status):
        order_ref = db.collection("orders").document(order_id)
        if not order_ref.get().exists:
            return {'message': 'Order not found'}, 404

        order_ref.update({
            'status': new_status
        })

    @classmethod
    def get_order_items(cls, order_id):
        order_items_ref = db.collection('orders').document(order_id).collection('order_items')
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
            return {'message': 'Order not found'}, 404

        order = cls.from_dict(doc_ref.to_dict())

        return order

    def delete(self):
        db.collection('orders').document(self.order_id).delete()

    def update_total_price(self):
        total = sum(order_item.get_amount() for order_item in self.get_order_items(self.order_id))
        order_ref = db.collection('orders').document(self.order_id)
        order_ref.update({
            'total_price': total
        })

    def add_order_item(self, order_item):
        order_item.save(self.order_id)
        self.update_total_price()

