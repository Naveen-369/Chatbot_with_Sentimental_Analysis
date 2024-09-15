class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, session_id):
        self.sessions[session_id] = {'context': []}

    def get_session(self, session_id):
        return self.sessions.get(session_id, None)

    def update_context(self, session_id, user_input, bot_response):
        if session_id in self.sessions:
            self.sessions[session_id]['context'].append((user_input, bot_response))

session_manager = SessionManager()
