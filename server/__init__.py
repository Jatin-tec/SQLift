from flask import Flask
from flask_cors import CORS
import os 
from dotenv import load_dotenv
from flask_socketio import SocketIO

load_dotenv() 

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")

    # Configure Flask-Mail settings
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
    app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")  # or the appropriate port number
    app.config['MAIL_USE_TLS'] = True  # or False if your server doesn't use TLS
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")


    with app.app_context():
        from server.auth import auth_bp
        from server.chat import chat_bp

        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(chat_bp, url_prefix='/chat')

        socketio = SocketIO(app)
        return app, socketio