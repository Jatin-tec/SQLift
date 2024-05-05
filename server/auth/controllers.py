from flask import jsonify, make_response, current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail
from passlib.hash import scrypt
import uuid
import datetime
import jwt

from server.utils import token_required
from flask_mail import Message
# from app.models.users import User
# from app import db


def register_user(data, *args, **kwargs):
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Invalid username or password'}), 400
    
    try:
        hashed_password = generate_password_hash(password, method='sha256')
        hashed_password = scrypt.hash(password)
        # new_user = User(public_id=str(uuid.uuid4()), username=username, password=hashed_password, admin=False)
        # db.session.add(new_user)
        # db.session.commit()
        return jsonify({'message': 'New user created!'}), 201
    
    except Exception as e:
        return jsonify({'message': 'Something went wrong', 'error': str(e)}), 500


def login_user(auth, *args, **kwargs):
    try :
        if not auth or not auth.username or not auth.password:
            return jsonify({'msg':'Could not verify'}), 401

        # user = User.query.filter_by(username=auth.username).first()

        # if not user:
        #     return jsonify({'msg':'Could not verify'}), 401
        
        # if scrypt.verify(auth.password, user.password):
        #     token = jwt.encode({
        #         'public_id' : user.public_id, 
        #         'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, 
        #         key=app.config['SECRET_KEY'], 
        #         algorithm="HS256")
          
            # return jsonify({'token' : token}), 200

        return jsonify({'error': 'Invalid username or password'}), 401
    
    except Exception as e:
        return jsonify({'message': 'Something went wrong', 'error': str(e)}), 500


def send_reset_email(username, *args, **kwargs):
    host_url = 'http://localhost:5000/'
    # user = User.query.filter_by(username=username).first()
    mail = Mail(app)  

    try:
        # if not user:
        #     return jsonify({'error': 'User not found'}), 404
        
        # Generate a password reset token
        payload = {
            'public_id': "user.public_id",
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        }
        reset_token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

        # Compose the email message
        subject = 'Password Reset Request'
        body = f'Click the link below to reset your password:\n\n{host_url}reset/{reset_token}'
        # recipients = [user.username]  # Replace with the user's email address

        # Send the email
        # message = Message(subject=subject, body=body, recipients=recipients, sender=app.config['MAIL_DEFAULT_SENDER'])
        # mail.send(message)
        
        return jsonify({'message': 'Password reset email sent'}), 200

    except Exception as e:
        return jsonify({'message': 'Something went wrong', 'error': str(e)}), 500


def reset_password(request):
    if 'x-access-token' in request.headers:
        reset_token = request.headers['x-access-token']

    new_password = request.json.get('new_password')

    if not reset_token or not new_password:
        return jsonify({'message' : 'Invalid request!'}), 401
    
    try:
        payload = jwt.decode(reset_token, app.config['SECRET_KEY'], algorithms=['HS256'])
        public_id = payload.get('public_id')

        # Retrieve the user from the database
        # user = User.query.filter_by(public_id=public_id).first()

        # if not user:
        #     return jsonify({'error': 'User not found'}), 404

        # Update the user's password
        hashed_password = scrypt.hash(new_password)
        # user.password = hashed_password
        # db.session.commit()

        return jsonify({'message': 'Password reset!'}), 201
    
    except Exception as e:
        return jsonify({'message': 'Something went wrong', 'error': str(e)}), 500


@token_required
def get_all_users(current_user, *args, **kwargs):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'}), 401
    try:
        # users = User.query.all()

        output = []

        # for user in users:
        #     user_data = {}
        #     user_data['public_id'] = user.public_id
        #     user_data['username'] = user.username
        #     user_data['admin'] = user.admin
        #     output.append(user_data)

        return jsonify({'users' : output}), 200
    
    except Exception as e:
        return jsonify({'message': 'Something went wrong', 'error': str(e)}), 500


@token_required
def get_user_by_id(user, *args, **kwargs):
    try:
        if not user:
            return jsonify({'message' : 'No user found!'})

        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['admin'] = user.admin

        return jsonify({'user' : user_data}), 200

    except Exception as e:
        return jsonify({'message': 'Something went wrong', 'error': str(e)}), 500