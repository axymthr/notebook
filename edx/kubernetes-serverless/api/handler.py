import numpy as np

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    a = np.array([1,2,3,4])
    b = np.array([1,2,3,4])
    return a.dot(b)
