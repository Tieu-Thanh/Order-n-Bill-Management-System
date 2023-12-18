from flask import request
from flask_restful import Resource, reqparse
from app.models import Order, OrderItem, db


class OrderItemResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('order_id', type=str, required=True)
        self.parser.add_argument('menu_item_id', type=str, help='Menu item ID', required=True)
        self.parser.add_argument('quantity', type=int, help='Quantity', required=True)
        self.parser.add_argument('special_request', type=str, help='Special request', default="")
        self.parser.add_argument('status', type=str, help='Status', default="pending")
        self.parser.add_argument('amount', type=float, help='Amount', default=None)

    def post(self):
        args = self.parser.parse_args()
        order_id = args['order_id']
        menu_item_id = args['menu_item_id']
        quantity = args['quantity']
        special_request = args['special_request']
        status = args['status']

        # Fetch order document from Firestore
        order_doc = db.collection('orders').document(order_id).get()
        order = Order.from_dict(order_doc.to_dict())

        # Add OrderItem to the order
        order.add_order_item(menu_item_id, quantity, special_request, status)

        return {'message': 'Order item added'}, 201


class OrderResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('order_id', type=str, help='Order ID', required=True)
        self.parser.add_argument('total_price', type=float, help='Total price', required=True)
        self.parser.add_argument('status', type=str, help='Status', default="pending")
        self.parser.add_argument('order_items', type=str, help='Ordered items', required=False)

    def post(self):
        args = self.parser.parse_args()
        order_id = args['order_id']
        total_price = args['total_price']
        status = args['status']

        # Create Order instance
        order = Order(order_id=order_id, order_items=[], total_price=total_price, status=status)
        db.collection('orders').document(order_id).set(order.to_dict())

        return {'order': order.to_dict()}, 201

    def get(self):
        try:
            orders = Order.get_orders()
            order_data = [order.to_dict() for order in orders]
            return {'orders': order_data}, 201
        except Exception as e:
            return {'message': str(e)}, 500


class OrderDetailResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('total_price', type=float, required=False)
        self.parser.add_argument('status', type=str, required=True)

    def put(self, order_id):
        args = self.parser.parse_args()
        new_status = args['status']

        # Fetch existing order from Firestore
        order_doc = db.collection('orders').document(order_id).get()
        if not order_doc.exists:
            return {'message': 'Order not found'}, 404

        # Update
        order = Order.from_dict(order_doc.to_dict())
        order.update_status(new_status)

        return {'order': order.to_dict()}, 201

    def get(self, order_id):
        order = Order.get_detail_order(order_id)
        return {'order': order.to_dict()}, 201

    def delete(self, order_id):
        order = Order.get_detail_order(order_id)
        if order:
            order.delete()
            return {'message': 'Successfully deleted order'}, 201
        else:
            return {'message': 'Order not found'}, 404
