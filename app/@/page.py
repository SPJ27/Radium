import json
from Radium.outputs import Outputs
from auth.auth import account

def page(req):
    session = account.get_session(req)
    response = json.loads(session.body)
    if session.status == '200 OK':
        return Outputs.HTMLResponse(f"<h1>Logged in as {response.get('email')}</h1><br><a href='/logout'>Logout</a>")
    return Outputs.HTMLFileResponse('templates/home.html', )