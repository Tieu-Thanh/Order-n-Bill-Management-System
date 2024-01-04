from flask import Blueprint
from flask_restful import Api
from app.api.resources.bill_resource import BillResource

bill_api_bp = Blueprint('bill_api', __name__)
api = Api(bill_api_bp)

api.add_resource(BillResource, '/', endpoint='bills')
