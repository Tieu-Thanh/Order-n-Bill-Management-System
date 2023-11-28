import firebase_admin
from flask import Flask, render_template
from config import app_config
from firebase_admin import credentials
from blueprints.order import order
from blueprints.menu import menu

app = Flask(__name__)
app.config.from_object(app_config)

# Initialize Firebase Admin SDK
cred = credentials.Certificate(app.config['FIREBASE_CREDENTIALS'])
firebase_admin.initialize_app(cred)

app.register_blueprint(order.order_bp, url_prefix='/order')
app.register_blueprint(menu.menu_bp, url_prefix='/menu')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
