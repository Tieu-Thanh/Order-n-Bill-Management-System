from flask import Flask, render_template, flash
from config import app_config, Config
from flask_restful import Api
from app.api.blueprints import diner_api, menu_api, order_api, bill_api
from app.api.models.MenuItem import MenuItem
from app.api.models import Order, OrderItem
# from app.models import MenuItem
from flask import request, jsonify
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import requests

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(app_config)
firebase_admin_instance = Config.FIRESTORE
app.config['FIREBASE_ADMIN'] = firebase_admin_instance

app.register_blueprint(menu_api.menu_api_bp, url_prefix='/api/menu')
app.register_blueprint(diner_api.diner_api_bp, url_prefix='/api/auth')
app.register_blueprint(order_api.order_api_bp, url_prefix='/api/orders')
app.register_blueprint(bill_api.bill_api_bp, url_prefix='/api/bills')


# @app.route('/')
# def hello_world():  # put application's code here
#     return render_template("index.html")

@app.route('/')
def index():
    menu_items = MenuItem.list_items()
    return render_template('home.html', menu_items=menu_items)

@app.route('/menu/<menu_item_id>')
def get_menu_item(menu_item_id):
    menu_item = MenuItem.get_item(menu_item_id)
    return render_template('menu_item.html', menu_item=menu_item)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item_data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'price': request.form['price'],
            'isOnStock': request.form.get('is_on_stock') == 'on',
            'category': request.form['category']
        }

        # Gọi API để thêm mục mới
        response = requests.post('http://your-api-endpoint/add_item', json=item_data)

        if response.status_code == 201:
            flash('Item added successfully!', 'success')
        else:
            flash(f'Failed to add item. Error: {response.json().get("error")}', 'error')

        # Redirect to the same add_item route to display the form again
        return render_template('add_item.html')

    return render_template('add_item.html')
@app.route('/kitchen')
def kitchen():
    return render_template('kitchen.html')

@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.json
    ordered_items = data['orderedItems']

    # Tạo đơn hàng mới trong Firestore
    order = Order.create_order(...)  # Thay ... bằng thông tin của đơn hàng (order)

    # Lưu thông tin về các món hàng đã đặt vào Firestore
    for item_data in ordered_items:
        order_item = OrderItem(**item_data)
        order_item.save(order.order_id)

    return jsonify({'message': 'Order placed successfully'}), 200

@app.route('/diner/<diner_id>')
def get_diner(diner_id):
    # Logic to fetch diner info by ID and render diner template
    pass




if __name__ == '__main__':
    app.run(debug=True)
