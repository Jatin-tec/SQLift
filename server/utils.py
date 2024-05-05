from functools import wraps
from flask import request, jsonify
from flask import current_app as app
# from server.models.users import User

import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(
                token, 
                app.config['SECRET_KEY'], 
                algorithms=["HS256"])
            # current_user = User.query.filter_by(public_id=data['public_id']).first()

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'token has expired'}), 401

        except (jwt.InvalidTokenError, Exception) as e:
            return jsonify({'error': 'Invalid reset token', 'message': str(e)}), 400
        
        return f("current_user", *args, **kwargs)    

    return decorated

def validate_email(email):
    if len(email) > 7:
        if '@' in email:
            return True
    return False

def validate_phone_number(phone_number):
    if len(phone_number) >= 11:
        return True
    return False