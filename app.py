from flask import Flask
from config import app_config
from flask_restful import Api
from app.api.blueprints import diner_api, menu
from app.api.resources.diner_resource import DinerResource

app = Flask(__name__)
app.config.from_object(app_config)
api = Api(app)

app.register_blueprint(menu.menu_bp, url_prefix='/menu')
app.register_blueprint(diner_api.diner_api_bp, url_prefix='/api/auth')


# Register DinerResource with the specified endpoint
api.add_resource(DinerResource, '/api/diner/register', endpoint='diner_resource')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
