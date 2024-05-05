from flask import Blueprint

chat_bp = Blueprint('chat', __name__)
from server.chat.views import handle_chat_message, handle_connection, handle_disconnect

from server import socketio

# Register Socket.IO events
socketio.on_namespace(handle_connection, '/chat')
socketio.on_namespace(handle_disconnect, '/chat')
socketio.on_namespace(handle_chat_message, '/chat')