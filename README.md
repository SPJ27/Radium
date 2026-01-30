# **Radium**

To install:
pip install radium-web

It is a lightweight Python web framework focused on **file-based routing**, **server-side rendering**, and **simple authentication**, designed for rapid development and learning.
⚠️ **v0.1 is for development only — not production-ready yet.**

---

## Features

### 1. Routing & Requests

* **File-Based Routing**
  Routes are automatically generated from the folder structure.
  Use `@` to define routes:

  ```
  @login
  @login/[id]
  ```
* **Params & Query Support**
  Built-in handling for dynamic route parameters and query strings.
* **HTTP Method Detection**
  Automatic detection of `GET`, `POST`, and other HTTP methods.

---

### 2. Request Object (`req`)

The `req` object provides structured access to incoming request data:

* `req.path` – Requested URL path
* `req.method` – HTTP method
* `req.body` – Parsed request body
* `req.query` – Query parameters
* `req.params` – Route parameters
* `req.headers` – Request headers
* `req.route` – Matched route
* `req.cookies` – Parsed cookies

---

### 3. Response Object (`res`)

The `res` object controls outgoing responses:

* `res.body` – Response body
* `res.status` – HTTP status code
* `res.headers` – Response headers
* `res.cookies` – Cookies to be sent
* `res.set_cookie(key, value)` – Set a cookie

---

### 4. Rendering & Outputs

* **Radium Templating Engine**
  Lightweight templating for dynamic HTML rendering.
* **Layout Support**
  Reusable layouts with child view injection.
* **Output Methods**

  * JSON responses
  * Plain text responses
  * Raw HTML responses
  * HTML file responses

---

### 5. Authentication & Security

* **Email Authentication**
  Built-in email-based authentication.
* **Authentication Sessions**
  Secure session handling for logged-in users.
* **Hashed Password Storage**
  Passwords are securely hashed before being stored.
* **Auth Utilities**
  Auth helpers are available via `auth.auth`.

---

### 6. Server & Middleware

* **Middleware Support**
  Global and route-level middleware.
* **Custom Error Pages**
  Supports custom error pages such as `&error.html`.
* **Static File Serving**
  Serve CSS, JS, images, and other static assets.
* **Auto Reload**
  Automatic server reload on file changes during development.

---

### 7. Developer Experience

* **CLI Tools**
  Command-line utilities for project setup and management.
* **Environment Variable Support (`.env`)**
  Built-in configuration using environment variables.

> ⚠️ **Supabase-related variables in `.env` MUST NOT be modified.**

---

## 📌 Usage Example

```python
import json
from Radium.outputs import Outputs
from auth.auth import account
from supabase_utils.setup import SupabaseSetup

def page(req):
    return Outputs.HTMLFileResponse(
        'templates/home.html'
    )
```

---

## ⚠️ Important Notes

* **File structure MUST NOT be changed**
* **v0.1 does not support production use**
* Routes must be created using the `@` prefix
* Auth functions should be accessed only from `auth.auth`
* Supabase environment variables must remain unchanged
