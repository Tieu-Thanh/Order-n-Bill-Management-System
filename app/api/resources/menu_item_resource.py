from flask_restful import Resource, reqparse
from firebase_admin import firestore
from app.models import MenuItem
from flask import request


class MenuItemResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, help='Menu item name', required=True)
        self.parser.add_argument('description', type=str, help='Menu item description', required=True)
        self.parser.add_argument('price', type=float, help='Menu item price', required=True)
        self.parser.add_argument('is_on_stock', type=bool, help='Menu item', default=True)
        self.parser.add_argument('category', type=str, help='Menu item category', required=True)

    def post(self):
        args = self.parser.parse_args()
        menuItem = MenuItem(**args)
        MenuItem.save(menuItem)
        return {'message': 'Menu item added successfully'}, 201

    def get(self):
        category = request.args.get('category')

        if category:
            menuItems = MenuItem.get_items_by_category(category)
        else:
            menuItems = MenuItem.list_items()

        menu_items_data = [item.to_dict() for item in menuItems]

        return {'menuItems': menu_items_data}, 200


class MenuItemDetailResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, help='Menu item name', required=True)
        self.reqparse.add_argument('description', type=str, help='Menu item description', required=True)
        self.reqparse.add_argument('price', type=str, help='Menu item price', required=True)
        self.reqparse .add_argument('is_on_stock', type=bool, help='Menu')
        self.reqparse .add_argument('category', type=str, help='Menu')

    def get(self, menu_item_id):
        print(f"Received menu_item_id: {menu_item_id}")
        menu_item = MenuItem.get_item(menu_item_id)
        if menu_item:
            return {'menuItem': menu_item.to_dict()}, 200
        else:
            return {'message': 'Not found Item'}, 404

    def put(self, menu_item_id):
        args = self.reqparse.parse_args()
        menu_item = MenuItem.get_item(menu_item_id)
        if menu_item:
            menu_item.update(**args)
            return {'message': 'Menu item updated successfully', 'menu_item': menu_item.to_dict()}
        else:
            return {'error': 'Menu item not found'}, 404

    def delete(self, menu_item_id):
        menu_item = MenuItem.get_item(menu_item_id)
        if menu_item:
            menu_item.delete()
            return {'message': 'Menu item deleted successfully'}
        else:
            return {'error': 'Menu item not found'}, 404
