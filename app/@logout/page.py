from auth.auth import account
from Radium.outputs import Outputs

def page(req):
    return account.logout(req)