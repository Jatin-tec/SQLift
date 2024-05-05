from flask import request
from server.auth.controllers import register_user, get_user_by_id, get_all_users, login_user, send_reset_email, reset_password

def register():
    data = request.get_json()
    response, code = register_user(data)
    return response, code

def login():
    auth = request.authorization
    response, code = login_user(auth)
    return response, code

def reset_password_mail():
    username = request.json['username']
    response, code = send_reset_email(username)
    return response, code

def get_users():
    response, code = get_all_users()
    return response, code

def get_user_detail():
    response, code = get_user_by_id()
    return response, code

def forgot_password():
    response, code = reset_password(request)
    return response, code