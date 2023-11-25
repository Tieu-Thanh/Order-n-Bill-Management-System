from flask import Blueprint, render_template

order_bp = Blueprint('order', __name__, static_folder='static', template_folder='templates')


@order_bp.route('/')
def index():
    return "<h1>Order</h1>"
