from server.wsgi import socketio

@socketio.on('connect')
def get_visual_chat():
    pass

@socketio.on('connect')
def get_chat():
    print('received message: ' + data)