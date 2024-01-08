from flask import Flask, render_template
from config import app_config, Config
from flask_restful import Api
from app.api.blueprints import diner_api, menu_api, order_api, bill_api
from app.api.models.MenuItem import MenuItem
# from app.models import MenuItem

app = Flask(__name__)
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

@app.route('/diner/<diner_id>')
def get_diner(diner_id):
    # Logic to fetch diner info by ID and render diner template
    pass

if __name__ == '__main__':
    app.run(debug=True)
