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
        self.parser.add_argument('bill_id', type=str, help='Bill ID', default="")
        self.parser.add_argument('ordered_items', type=list, location="json", help='List of order items')

    def post(self):
        args = self.parser.parse_args()
        order_id = args['order_id']
        total_price = args['total_price']
        status = args['status']
        bill_id = args['bill_id']
        ordered_items = args.get('ordered_items', [])

        # Create Order instance
        order = Order(order_id, total_price, bill_id, status)
        order.save()

        # Add order items to the Order instance
        for item in ordered_items:
            order_item = OrderItem(**item)  # Assuming OrderItem initialization accepts a dictionary
            order_item.save(order_id)

        return {'order': order.to_dict()}, 201

    def get(self):
        try:
            orders = Order.get_orders()
            order_data = []
            for order in orders:
                order_dict = order.to_dict()
                order_dict['ordered_items'] = [item.to_dict() for item in Order.get_ordered_items(order.order_id)]
                order_data.append(order_dict)
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

        order = Order.get_order_by_id(order_id)
        if order is None:
            return {'message': 'Order not found'}, 404

        order.update_status(new_status)

        return {'message': 'Order updated successfully'}, 201

    def get(self, order_id):
        order = Order.get_order_by_id(order_id)

        if order is None:
            return {'message': 'Order not found'}, 404

        order_data = order.to_dict()

        order_data['ordered_items'] = [item.to_dict() for item in Order.get_ordered_items(order_id)]

        return {'order': order_data}, 201

    def delete(self, order_id):
        order = Order.get_order_by_id(order_id)
        if order is None:
            return {'message': 'Order not found'}, 404

        order.delete()
        return {'message': 'Successfully deleted order'}, 201
