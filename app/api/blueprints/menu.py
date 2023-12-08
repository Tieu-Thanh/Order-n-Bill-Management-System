from flask import Blueprint, request, jsonify
from app.models import MenuItem


menu_bp = Blueprint('menu', __name__)


@menu_bp.route('/add_item', methods=['POST'])
def add_menu_item():
    data = request.get_json()

    # Create a MenuItem instance
    menu_item = MenuItem(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        is_on_stock=data.get('isOnStock', True),
        category=data.get('category')
    )

    # Call the save method to add the item to Firestore
    saved_menu_item = MenuItem.save(menu_item)

    # Return a response with the document ID
    return jsonify({'name': saved_menu_item.name, 'message': 'Successfully added!'}), 201


@menu_bp.route('/list_items', methods=['GET'])
def list_menu_items():
    menu_items = MenuItem.list_items()

    menu_item_list = [item.to_dict() for item in menu_items]

    return jsonify(menu_item_list), 200
