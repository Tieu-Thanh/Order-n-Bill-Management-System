from flask import Blueprint
from app.api.resources.order_resource import OrderItemResource, OrderResource, OrderDetailResource
from flask_restful import Api

order_api_bp = Blueprint('order_api', __name__)
api = Api(order_api_bp)

api.add_resource(OrderResource, '/', endpoint='orders')
api.add_resource(OrderDetailResource, '/<string:order_id>', endpoint='order_detail')
api.add_resource(OrderItemResource, '/<string:order_id>/items/<string:menu_item_id>', endpoint='ordered_item')