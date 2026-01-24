from response import Response
import bcrypt
import uuid

class Outputs:
    def TextResponse(response):
        return Response(response, content_type="text/plain")

    def HTMLResponse(response):
        return Response(response, content_type="text/html") 

    def HTMLFileResponse(file_path, layout=None, params=None, layout_params=None):
        try:
            with open(f'./app/{file_path}', "r") as f:
                content = f.read()
            if params:
                for key, value in params.items():
                    content = content.replace(f"{{{{{key}}}}}", value)
            print("params:", params)
            print("content:", content)

            if layout:
                with open(f'./app/{layout}', "r") as f:
                    layout_content = f.read()

                if layout_params:
                    for key, value in layout_params.items():
                        layout_content = layout_content.replace(f"{{{{{key}}}}}", value)

                layout_content = layout_content.replace("{{children}}", content)
                
            return Response(layout_content, content_type="text/html")
        except FileNotFoundError:
            return Response(f"<h1>File {file_path} not found.</h1>", content_type="text/html")
        
    def JSONResponse(response_dict, cookies=None):
        import json
        res = Response(json.dumps(response_dict), content_type="application/json")
        if cookies:
            for key in cookies.keys():
                print('setting cookie', key, cookies[key])
                value = cookies[key]
                value = str(value)

                res.set_cookie(key=key, value=value)
        return res

    def redirectResponse(location, status="302 Found"):
        return Response("", status=status, headers=[("Location", location)])


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
    
    def get_session(self, request):
        try:
            print('cookies: ', request.cookies)
            email = self.sessions[request.cookies['session_id']]
            print('email', email)
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

