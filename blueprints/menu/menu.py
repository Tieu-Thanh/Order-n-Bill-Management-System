from flask import Blueprint

menu_bp = Blueprint('menu', __name__, static_folder='static', template_folder='templates')


@menu_bp.route('/')
def index():
    return "<h1>Menu Page</h1>"
