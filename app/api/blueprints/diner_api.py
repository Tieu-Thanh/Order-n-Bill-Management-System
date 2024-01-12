from flask import Blueprint
from flask_restful import Api
from app.api.resources.diner_resource import DinerResource

diner_api_bp = Blueprint('diner_api', __name__)
api = Api(diner_api_bp)

api.add_resource(DinerResource, '/', endpoint='diners')

