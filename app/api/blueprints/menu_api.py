from flask import Blueprint
from app.api.resources.menu_item_resource import MenuItemResource, MenuItemDetailResource
from flask_restful import Api

menu_api_bp = Blueprint('menu_api', __name__)
api = Api(menu_api_bp)

api.add_resource(MenuItemResource, '/items', endpoint='menu_items')
api.add_resource(MenuItemDetailResource, '/items/<string:menu_item_id>', endpoint='menu_item_detail')
