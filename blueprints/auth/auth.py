from flask import Blueprint, request, render_template
from firebase_admin import auth


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def home():
    return render_template('home.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = auth.get_user_by_email(email)
        return f'Hi {user.uid}'
    return render_template('login.html')
    pass


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # create user
        user = auth.create_user(
            email=email,
            password=password
        )

        return f'{user.uid} is created.'

    return render_template('register.html')
@auth_bp.route('/logout')
def logout():
    return 'Signed out.'
