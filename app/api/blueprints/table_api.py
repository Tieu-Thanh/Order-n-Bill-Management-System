from flask import Blueprint
from flask_restful import Api
from app.api.resources.table_resource import TableResource

table_api_bp = Blueprint('table_api', __name__)
api = Api(table_api_bp)

api.add_resource(TableResource, '/', endpoint='table')
