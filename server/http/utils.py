import ast
import logging

from server.http.const import reason_phrase


class HttpRequest:
    def __init__(self, method, path, ver, headers: dict, body=""):
        self.method = method
        self.path = path
        self.ver = ver
        self.headers = headers
        self.body = body


class HttpRespBuilder:
    def __init__(self, status_code):
        self.headers = {}
        self.body = b""
        self.status = f"HTTP/1.1 {status_code} {reason_phrase.get(status_code, 500)}\r\n".encode()

    def add_header(self, key: str, value: str):
        self.headers[key] = value
        return self

    def add_to_body(self, content):
        self.body = self.body + str(content).encode()
        return self

    def compile(self):
        concat_headers = b"".join([f"{k}: {self.headers[k]}\r\n".encode() for k in self.headers])
        return b"".join([self.status, concat_headers, b"\r\n", self.body])


def parse_http_req(req: str):
    start_line, header_body = req.split('\r\n', 1)
    headers, body = header_body.split('\r\n\r\n', 1)
    method, path, version = start_line.split(' ', 2)
    headers_dict = dict([tuple(h.split(": ", 1)) for h in headers.split("\r\n")])
    return HttpRequest(method, path, version, headers_dict, body)


def interpret(code):
    block = ast.parse(code, mode='exec')
    last = ast.Expression(block.body.pop().value)
    _globals, _locals = {}, {}
    exec(compile(block, '<string>', mode='exec'), _globals, _locals)
    return eval(compile(last, '<string>', mode='eval'), _globals, _locals)


def logger(func):
    def handle(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return ret
        except Exception as e:
            logging.error(str(e))
            return HttpRespBuilder(500).compile()

    return handle
