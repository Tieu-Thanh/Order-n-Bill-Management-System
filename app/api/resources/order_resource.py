from flask import request
from flask_restful import Resource, reqparse
from app.models import Order, db
from app.api.models.OrderItem import OrderItem
from app.api.models.Order import Order


class OrderItemResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('quantity', type=int, help="Quantity to order")
        self.parser.add_argument('special_request', type=str, help='Special request', default="")
        self.parser.add_argument('status', type=str, help='Status', default="pending")

    def post(self, order_id, menu_item_id):
        args = self.parser.parse_args()
        quantity = args['quantity']
        special_request = args['special_request']

        # Save the order item
        order_item = OrderItem(
            menu_item_id=menu_item_id,
            quantity=quantity,
            special_request=special_request
        )

        # Add item to Order
        order = Order.get_detail_order(order_id)
        if order:
            order.add_order_item(order_item)

        return {'message': 'Order item added'}, 201

    def put(self, order_id, menu_item_id):
        try:
            args = self.parser.parse_args()
            new_status = args['status']

            order_item = OrderItem.get_by_id(order_id, menu_item_id)
            if not order_item:
                return {"message": "Order item not found"}, 404

            order_item.update_status(new_status, order_id)

            return {'message': 'Order item updated'}, 200

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"message": str(e)}, 500


class OrderResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('order_id', type=str, help='Order ID', required=True)
        self.parser.add_argument('total_price', type=float, help='Total price', default=0.0)
        self.parser.add_argument('status', type=str, help='Status', default="pending")

    def post(self):
        args = self.parser.parse_args()
        order_id = args['order_id']
        total_price = args['total_price']
        status = args['status']

        # Create Order instance
        order = Order(order_id=order_id, total_price=total_price, status=status)
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
        self.parser.add_argument('status', type=str, required=True)

    def put(self, order_id):
        args = self.parser.parse_args()
        new_status = args['status']

        Order.update_status(order_id, new_status)
        return {'message': 'Order updated successfully'}, 201

    def get(self, order_id):
        order = Order.get_detail_order(order_id)
        if not order:
            return {'message': 'Order not found'}, 404

        order_data = order.to_dict()
        order_data['order_items'] = [item.to_dict() for item in Order.get_order_items(order_id)]

        return {'order': order_data}, 201

    def delete(self, order_id):
        order = Order.get_detail_order(order_id)
        if not order:
            return {'message': 'Order not found'}, 404

        order.delete()
        return {'message': 'Successfully deleted order'}, 201
