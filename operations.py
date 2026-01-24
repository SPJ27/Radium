from wsgiref.simple_server import make_server


class Server:
    def __init__(self):
        self.routes = {}

    def route(self, path):
        def decorator(fn):
            self.routes[path] = fn
            return fn
        return decorator
    def __call__(self, environ, start_response):
        path = environ["PATH_INFO"]
        handler = self.routes.get(path)

        if not handler:
            start_response("404 Not Found", [])
            return [b"Not Found"]
        start_response("200 OK", [("Content-Type", "text/plain")])
        return [handler().encode()]

app = Server()

@app.route("/hello")
def hello_handler():
    return {"message": "Hello from my framework"}