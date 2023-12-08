from flask import Blueprint
from app.api.resources.diner_resource import DinerResource

diner_api_bp = Blueprint('diner_api', __name__)

diner_api_bp.add_url_rule('/register', view_func=DinerResource.as_view('diner_resource'))
