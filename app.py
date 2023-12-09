from flask import Flask
from config import app_config, Config
from flask_restful import Api
from app.api.blueprints import diner_api, menu_api
from app.api.resources.diner_resource import DinerResource
from app.api.resources.menu_item_resource import MenuItemResource, MenuItemDetailResource


app = Flask(__name__)
app.config.from_object(app_config)
firebase_admin_instance = Config.FIRESTORE
app.config['FIREBASE_ADMIN'] = firebase_admin_instance


app.register_blueprint(menu_api.menu_api_bp, url_prefix='/api/menu')
app.register_blueprint(diner_api.diner_api_bp, url_prefix='/api/auth')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
