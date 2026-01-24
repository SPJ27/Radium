from wsgiref.simple_server import make_server
from app.paths import paths
import re
from request_class import Request

def normalize_response(response):
    # Format: [body, content_type]
    if len(response) == 2:
        body, content_type = response
        return body, "200 OK", [("Content-Type", content_type)]

    # Format: [body, content_type, status, headers]
    if len(response) == 4:
        body, content_type, status, headers = response

        if content_type:
            headers.append(("Content-Type", content_type))

        return body, status, headers

    raise ValueError("Invalid response format")


def match_route(route, path):
    pattern = re.sub(r"\[(\w+)\]", r"(?P<\1>[^/]+)", route.strip("/"))
    match = re.match(f"^{pattern}$", path.strip("/"))
    return match.groupdict() if match else None

def find_matching_route(routes, user_path):
    for route in routes:
        params = match_route(route, user_path)
        if params is not None:
            return route, params
    return None, None


def app(environ, start_response):
    request = Request(paths, environ)

    if request.route is None:
        try:
            with open("static/&error.html", "r") as f:
                error_content = f.read()
            start_response("404 Not Found", [("Content-Type", "text/html")])
            return [error_content.encode()]
        except FileNotFoundError:
            start_response("404 Not Found", [])
            return [b"Path Not Found"]
    
    function = paths[request.route]
    response = function(request)
    start_response(response.status, response.headers)
    return [response.body.encode()]


server = make_server("127.0.0.1", 8000, app)
server.serve_forever()
