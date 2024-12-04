from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit
from googletrans import Translator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,async_mode='eventlet')
translator = Translator()

clients = {}

@app.route('/')
def index():
    return render_template('chat.html')

@socketio.on('connect')
def handle_connect():
    print("A user connected!")

@socketio.on('join')
def handle_join(data):
    username = data.get('username')
    room = data.get('room')
    clients[username] = room
    print(f"{username}: {room}: {clients}")
    join_room(room)
    emit('message', {'sender': 'System', 'message': f'{username} has joined the room!'}, room=room)

@socketio.on('message')
def handle_message(data):
    sender = data.get('sender')
    room = data.get('room')
    msg = data.get('message')
    lang = data.get('lang')
    print(f"{sender}: {room}: {msg}")

    # Translate the message if a language is specified
    translated_message = translator.translate(msg, dest=lang).text if lang else msg
    emit('message', {'sender': sender, 'message': translated_message}, room=room)

@socketio.on('leave')
def handle_leave(data):
    username = data.get('username')
    room = data.get('room')
    leave_room(room)
    emit('message', {'sender': 'System', 'message': f'{username} has left the room!'}, room=room)

if __name__ == '__main__':
    socketio.run(app) 
    # print(clients)
