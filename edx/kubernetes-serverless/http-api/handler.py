import json

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    res = {"status": "ok"}
    res["status"] = "resource not found"
    code = 404
    return (
      json.dumps(res),
      code,
      {"Content-Type": "application/json"},
    )
