from Radium.outputs import Outputs
from auth.auth import account
import json
def page(req):
    if req.method == 'POST':
        email = req.body.get('email')
        password = req.body.get('password')
        login = account.login(email, password)
        print(login.status)
        if login.status != '302 Found':
            return Outputs.HTMLResponse("<h1>Invalid credentials</h1><a href='/login'>Go back</a>")
        return login
    
    return Outputs.HTMLFileResponse('templates/login.html')