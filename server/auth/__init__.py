from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
from server.auth.views import register, login, get_user_detail, get_users, reset_password_mail, forgot_password

# Register the routes
auth_bp.add_url_rule('/register', methods=['POST'], view_func=register)
auth_bp.add_url_rule('/login', methods=['POST'], view_func=login)
auth_bp.add_url_rule('/reset-password-mail', methods=['POST'], view_func=reset_password_mail)
auth_bp.add_url_rule('/forgot-password', methods=['POST'], view_func=forgot_password)
auth_bp.add_url_rule('/users', methods=['GET'], view_func=get_users)
auth_bp.add_url_rule('/user', methods=['GET'], view_func=get_user_detail)