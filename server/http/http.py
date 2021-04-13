import socket
import asyncio
import logging
from email.utils import formatdate
from .const import reason_phrase
from .utils import parse_http_req, HttpRequest, interpret


class HttpReqHandler:
    def __init__(self, request: HttpRequest):
        self.request = request

    def __on_get(self):
        return HttpRespBuilder(200) \
            .add_header('Server', 'ProChat') \
            .add_header('Content-Type', 'text/html; charset=utf-8') \
            .add_header('Access-Control-Allow-Origin', '*') \
            .add_header('Date', formatdate(timeval=None, localtime=False, usegmt=True)) \
            .add_to_body("<html><body>Hello coder!</body></html>")\
            .compile()

    def __on_post(self):
        result = interpret(self.request.body)
        return HttpRespBuilder(200) \
            .add_header('Server', 'ProChat') \
            .add_header('Content-Type', 'text/html; charset=utf-8') \
            .add_header('Access-Control-Allow-Origin', '*') \
            .add_header('Date', formatdate(timeval=None, localtime=False, usegmt=True)) \
            .add_to_body(f"<html><body>The result is {str(result)}</body></html>") \
            .compile()

    def handle(self):
        if self.request.method == 'GET':
            return self.__on_get()
        if self.request.method == 'POST':
            return self.__on_post()
        return HttpRespBuilder(501).compile()


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


class Session:
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr

    async def resolve(self):
        payload = self.sock.recv(1024).decode()
        logging.info(payload)

        parsed = parse_http_req(payload)
        resp = HttpReqHandler(parsed).handle()

        self.sock.send(resp)
        self.sock.close()


class HttpServer:
    HTTP_HOST = "127.0.0.1"
    HTTP_PORT = 8080

    @classmethod
    def serve(cls):
        http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        http_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        http_socket.bind((cls.HTTP_HOST, cls.HTTP_PORT))
        http_socket.listen(1)
        while True:
            c_conn, c_addr = http_socket.accept()
            session = Session(c_conn, c_addr)
            asyncio.run(session.resolve())
