from Radium.outputs import Outputs

def page(req):
    return Outputs.HTMLFileResponse(file_path='templates/home.html', layout='templates/_layout.html')
