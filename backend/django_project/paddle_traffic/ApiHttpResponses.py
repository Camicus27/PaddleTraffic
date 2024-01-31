from django.http import HttpResponse

"""
Status Codes
200 OK: Successful request and processing of JSON data.
400 Bad Request: Invalid JSON data.
405 Method Not Allowed: Request method other than POST is not allowed.
404 Not Found
415 Unsupported Media Type: Requested content type (JSON) is not supported.
"""


def http_ok(msg):
    return HttpResponse(msg, status=200, content_type="text/plain")  # OK


def http_bad_request_json():
    return HttpResponse("Invalid JSON data", status=400, content_type="text/plain")  # Bad Request


def http_bad_argument(msg):
    return HttpResponse("Bad Argument: " + msg, status=400, content_type="text/plain")


def http_ok_request_json():
    return HttpResponse("Received and processed JSON data", status=200, content_type="text/plain")  # OK


def http_unsupported_media():
    return HttpResponse("Unsupported Media Type", status=415, content_type="text/plain")  # Unsupported Media Type


def http_method_not_allowed():
    return HttpResponse("Method Not Allowed", status=405, content_type="text/plain")  # Method Not Allowed


def http_not_found(msg):
    return HttpResponse(msg + "Not Found", status=404, content_type="text/plain")


def http_unauthorized():
    return HttpResponse(status=401)

def HttpIAmATeapot(msg):
    return HttpResponse("I am a teapot", status=418, content_type="text/plain")
