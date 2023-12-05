from flask import Blueprint
from firebase_admin import auth

auth_bp = Blueprint('auth', __name__)
