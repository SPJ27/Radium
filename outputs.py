from response import Response

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
            res.set_cookie(key, cookies[key])
    return res

def redirectResponse(location, status="302 Found"):
    return Response("", status=status, headers=[("Location", location)])
