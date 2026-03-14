# Radium

Radium is a Python web framework built with Next.js routing system, becuase I hate Django (just kidding haha wait that wasn't funny). Instead of adding routes in a separate file, you create folders and write page functions.

---

## Installation

```bash
pip install radium-web
```

Then start a new project:

```bash
radium init myapp
cd myapp
python run.py
```

Radium has hot reload bydefault, so the server restarts automatically whenever you save a file.

---

## Routing

Routes are defined by the folder structure inside your `app/` directory. To create a new route, add a folder named `@pathName` and place a `page.py` file inside it with a function called `page`.

```python
# app/@home/page.py
from Radium.outputs import Outputs

def page(req):
    return Outputs.HTMLFileResponse('templates/home.html')
```

The folder name (without the `@`) becomes the URL path. Nested folders produce nested routes.

---

## The Request Object

Every `page` function receives a `req` object that gives you access to everything about the incoming request.

| Attribute | Description |
|---|---|
| `req.path` | The requested URL path |
| `req.method` | HTTP method (GET, POST, etc.) |
| `req.body` | Parsed request body |
| `req.query` | Query string parameters |
| `req.params` | Route parameters |
| `req.headers` | Request headers |
| `req.route` | The matched route |
| `req.cookies` | Parsed cookies |

---

## The Response Object

The `res` object controls what gets sent back to the client. This is generally built automatically by Output Response

| Attribute / Method | Description |
|---|---|
| `res.body` | Response body |
| `res.status` | HTTP status code |
| `res.headers` | Response headers |
| `res.cookies` | Cookies to send |
| `res.set_cookie(key, value)` | Set a cookie |

---

## Outputs

`Outputs` is the standard way to return a response from a `page` function. There are four types.

**HTML file** — renders a file from disk:
```python
return Outputs.HTMLFileResponse('./templates/home.html')
```

**Inline HTML** — renders a string directly:
```python
return Outputs.HTMLResponse('<h1>Hello</h1>')
```

**Plain text:**
```python
return Outputs.TextResponse('Hello')
```

**JSON:**
```python
return Outputs.JSONResponse({'key': 'value'})
```

---

## Layouts and Templating

You can wrap a page in a shared layout by passing a `layout` argument. The layout file is a plain HTML file with a `{{children}}` placeholder where the page content will be put in.

```python
return Outputs.HTMLFileResponse(
    './templates/home.html',
    layout='./templates/_layout.html'
)
```

```html
<!-- templates/_layout.html -->
<html>
<head>
  <title>My App</title>
</head>
<body>
  <nav>My Nav</nav>
  {{children}}
</body>
</html>
```

You can pass dynamic data to both the page and the layout using the `params` and `layoutParams` arguments:

```python
return Outputs.HTMLFileResponse(
    path='./templates/home.html',
    layout='./templates/_layout.html',
    params={'title': 'Welcome'},
    layoutParams={'user': 'Alice'}
)
```

```html
<h1>{{title}}</h1>
```

---

## Authentication

Each route folder has access to an `account` object imported from `auth.auth`. This gives you everything you need to handle user sessions automatically.

```python
from auth.auth import account
```

Available methods:

- `account.create_account(email, password)` — registers a new user
- `account.login(email, password)` — authenticates and starts a session
- `account.logout(request)` — ends the current session
- `account.get_session(request)` — retrieves the active session

Passwords are never stored in plain text. Radium encrypts and hashes them before persisting.

---

## Custom Error Pages

To show a branded error page instead of the default one, create a file at `templates/&error.html`. Radium will render it automatically whenever an error occurs.

---

## Project Structure

```
myapp/
├── app/
│   ├── @home/
│   │   └── page.py
│   └── @dashboard/
│       └── page.py
├── templates/
│   ├── _layout.html
│   ├── home.html
│   └── &error.html
├── auth/
│   └── auth.py
└── run.py
```