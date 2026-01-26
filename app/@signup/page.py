from Radium.outputs import Outputs
from auth.auth import account

def page(req):
    if req.method == 'POST':
        email = req.body.get('email')
        password = req.body.get('password')
        new_account = account.create_account(email, password)
        if new_account.status == '409 Conflict':
            return Outputs.HTMLResponse("<h1>Account already exists</h1><a href='/signup'>Go back</a>")
        return Outputs.HTMLResponse("<h1>Account created successfully</h1><a href='/login'>Login</a>")
    return Outputs.HTMLFileResponse('templates/signup.html')
