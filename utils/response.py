from rest_framework.response import Response

def AssertionErrorResponse(msg=None):
    status = 400
    resp = generateResponse("error")
    if msg:
        message = msg.split("::")
        resp['message'] = message[0]
        status = int(message[1])
    return Response(resp, status = status)

def ErrorResponse(msg=None, status_code=400):
    resp = generateResponse("error")
    if msg:
        resp['message'] = msg
    return Response(resp, status = status_code)

def generateResponse(status):
    return {"status": status}

def SuccessResponse(data, **kwargs):
    data['status'] = "success"
    return Response(data, **kwargs)