import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from models import ChatLog, session
from utils import analyze_sentiment
from session_manager import session_manager
import uuid
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    try:
        session_id = str(uuid.uuid4())
        session_manager.create_session(session_id)
        emit('session_id', {'session_id': session_id})
    except Exception as e:
        logging.error(f"Error during connect event: {e}")

@socketio.on('user_message')
def handle_message(data):
    try:
        session_id = data.get('session_id')
        user_input = data.get('message')

        if not session_id or not user_input:
            logging.error("Missing session_id or user_input in message data")
            return

        print(user_input)
        print(analyze_sentiment(user_input))
        sentiment, score = analyze_sentiment(user_input)
        
        print(score,sentiment)

        # Convert the score to a standard Python float
        score = float(score)

        if sentiment == 'POSITIVE':
            response = "I'm glad you're feeling good!"
        elif sentiment == 'NEGATIVE':
            response = "I'm sorry to hear that."
        elif sentiment == 'NEUTRAL':
            response = "Thanks for sharing your thoughts!"
        else:
            response = "I'm not sure how to respond to that."

        chat_log = ChatLog(user_input=user_input, bot_response=response, sentiment=sentiment, score=str(score))
        session.add(chat_log)
        session.commit()

        session_manager.update_context(session_id, user_input, response)
        emit('bot_response', {'response': response, 'sentiment': sentiment, 'score': score})
    except Exception as e:
        logging.error(f"Error during user_message event: {e}")
        emit('error', {'error': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True)
