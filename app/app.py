from response import Response
from Radium import AccountSystem
from Radium import Outputs
import json

account = AccountSystem()

def home(req):
    user = account.get_session(req)
    user_data = json.loads(user.body)
    print('user in home:', user_data)
    if user:
        return Outputs.HTMLResponse(f"<h1>Welcome {user_data['email']}</h1><a href='/logout'>Logout</a>")

    return Outputs.HTMLResponse("""
        <h1>Home</h1>
        <a href="/signup">Signup</a><br>
        <a href="/login">Login</a>
    """)

def signup(req):
    if req.method == "POST":
        print(req.body)
        email = req.body.get("email")
        password = req.body.get("password")
        account.create_account(email=email, password=password)
        return Outputs.TextResponse("Signup successful")

    return Outputs.HTMLResponse("""
        <form method="POST">
            Email: <input name="email"><br>
            Password: <input name="password" type="password"><br>
            <button>Signup</button>
        </form>
    """)


def login(req):
    if req.method == "POST":
        email = req.body.get("email")
        password = req.body.get("password")
        sid = account.login(email, password)
        print('body', (sid.body))
        if json.loads(sid.body)['message'] != "verified":
            return Outputs.TextResponse("Invalid credentials")
        return sid

    return Outputs.HTMLResponse("""
        <form method="POST">
            Email: <input name="email"><br>
            Password: <input name="password" type="password"><br>
            <button>Login</button>
        </form>
    """)

