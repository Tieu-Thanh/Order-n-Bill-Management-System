from flask import Flask
from config import app_config, Config
from flask_restful import Api
from app.api.blueprints import diner_api, menu_api, order_api, bill_api

app = Flask(__name__)
app.config.from_object(app_config)
firebase_admin_instance = Config.FIRESTORE
app.config['FIREBASE_ADMIN'] = firebase_admin_instance

app.register_blueprint(menu_api.menu_api_bp, url_prefix='/api/menu')
app.register_blueprint(diner_api.diner_api_bp, url_prefix='/api/auth')
app.register_blueprint(order_api.order_api_bp, url_prefix='/api/orders')
app.register_blueprint(bill_api.bill_api_bp, url_prefix='/api/bills')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
