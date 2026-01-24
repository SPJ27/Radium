from app.app import *

paths = {
    "/": homepage,
    "/add/[item]": addItem,
    '/signup': signUp,
    '/login': getLogin
}