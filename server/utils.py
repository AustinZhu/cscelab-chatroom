import json


class HttpRequest:
    def __init__(self, method, path, ver, headers: dict, body=""):
        self.method = method
        self.path = path
        self.ver = ver
        self.headers = headers
        self.body = body


def parse_http_req(req: str):
    start_line, header_body = req.split('\r\n', 1)
    headers, body = header_body.split('\r\n\r\n', 1)
    method, path, version = start_line.split(' ', 2)
    headers_dict = dict([tuple(h.split(": ", 1)) for h in headers.split("\r\n")])
    return HttpRequest(method, path, version, headers_dict, body)
