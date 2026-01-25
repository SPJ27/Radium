import bcrypt
import uuid
from Radium.outputs import Outputs

class AccountSystem:
    """
    So how does this work?
    store session_id in cookie
    in a dict store session id and user email
    to get user get the session id and get the email from the dict
    """
    def __init__(self):
        self.users = {} # This stores email and hashed paasword
        self.sessions = {} # stores sessions id and email

    """
    this reloads after every server restart
    so use a database so that you don't lose data
    """

    """
    after login, get the session id from cookies
    get the email from sessions list

    hashed passwords are only for login and account creation
    users dict stores email and hashed password
    to login match the password with hashed
    """

    def create_account(self, email, password):
        if email in self.users:
            return Outputs.JSONResponse({'status': '402', 'message': 'exist'})
        self.users[email] = self.hash_password(password)
        response = Outputs.JSONResponse({'status': '200 OK', 'message': 'created'})
        print(self.users)
        return response

    def login(self, email, password):
        if email not in self.users:
            return Outputs.JSONResponse({'status': '402', 'message': 'exist'})
        if self.verify_password(password, self.users[email]):
            session_id = uuid.uuid4().hex
            self.sessions[session_id] = email
            return Outputs.JSONResponse({'status': '200 OK', 'message': 'verified'}, {'session_id': session_id})
        return Outputs.JSONResponse({'status': '402', 'message': 'invalid'})
    
    def logout(self, request):
        session_id = request.cookies['session_id']
        if session_id in self.sessions:
            del self.sessions[session_id]
        res = Outputs.JSONResponse({'status': '200 OK', 'messgage': 'done'}, {'session_id': ''})
        return res

    def get_session(self, request):
        try:
            email = self.sessions[request.cookies['session_id']]
            if email is not None:
                return Outputs.JSONResponse({'status': '200 OK', 'email': email, 'message': 'success'})
        except:
            return Outputs.JSONResponse({'status': '402', 'message': 'failed'})

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()


    def verify_password(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(
            password.encode(),
            hashed.encode()
        )

