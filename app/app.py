from outputs import HTMLFileResponse, redirectResponse, HTMLResponse, JSONResponse
from response import Response
listOfItems = ['12']

def homepage(res):
    global listOfItems
    item = res.params.get('item')
    return HTMLFileResponse('/static/home.html', layout='/static/_layout.html', params={'item': item}, layout_params={'title': 'Home Page'})

def addItem(res):
    global listOfItems
    item = res.headers.get('item')
    # print(res.headers)
    listOfItems.append(item)
    return redirectResponse("/")

def signUp(req):
    return JSONResponse({'status': '200 OK', 'creation': 'successful'}, cookies={'email': 'saksham.khatod27@gmail.com', 'password': 'hello.123'})

def getLogin(req):
    print('cookies: ', req.cookies)
    return JSONResponse({'1': 2})