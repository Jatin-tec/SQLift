from flask import request
from server import socketio

@socketio.on('connect')
def handle_connection(sid):
    # Handle connection event
    print('Client connected with ID:', sid)

@socketio.on('disconnect')
def handle_disconnect(sid):
    # Handle disconnect event
    print('Client disconnected with ID:', sid)

@socketio.on('chat message')
def handle_chat_message(sid, message):
    # Handle chat message event
    print('Client with ID:', sid, 'sent message:', message)