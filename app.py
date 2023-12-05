from flask import Flask
from config import app_config

from blueprints.menu import menu


app = Flask(__name__)
app.config.from_object(app_config)

app.register_blueprint(menu.menu_bp, url_prefix='/menu')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
