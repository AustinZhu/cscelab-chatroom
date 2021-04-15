import socket
import asyncio
import logging
import json
from email.utils import formatdate
from .utils import parse_http_req, HttpRequest, interpret, logger, HttpRespBuilder


class HttpReqHandler():

    def __init__(self, request: HttpRequest):
        self.request = request

    @logger
    def __on_get(self):
        return HttpRespBuilder(200) \
            .add_header('Server', 'ProChat') \
            .add_header('Content-Type', 'text/html; charset=utf-8') \
            .add_header('Access-Control-Allow-Origin', '*') \
            .add_header('Date', formatdate(timeval=None, localtime=False, usegmt=True)) \
            .add_to_body("<html><body>Hello coder!</body></html>") \
            .compile()

    @logger
    def __on_post(self):
        code = json.loads(self.request.body).get("code")
        result = interpret(code)
        return HttpRespBuilder(200) \
            .add_header('Server', 'ProChat') \
            .add_header('Content-Type', 'text/html; charset=utf-8') \
            .add_header('Access-Control-Allow-Origin', '*') \
            .add_header('Date', formatdate(timeval=None, localtime=False, usegmt=True)) \
            .add_to_body(f"<html><body>Your message is:<br>{str(result)}</body></html>") \
            .compile()

    def handle(self):
        if self.request.method == 'GET':
            return self.__on_get()
        if self.request.method == 'POST':
            return self.__on_post()
        return HttpRespBuilder(501).compile()


class Session:
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        logging.info(f"Coming Request from {addr}")

    async def resolve(self):
        payload = self.sock.recv(1024).decode()
        req = parse_http_req(payload)
        resp = HttpReqHandler(req).handle()
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
        logging.info(f"Server started on port {cls.HTTP_PORT}")
        http_socket.listen(1)
        while True:
            c_conn, c_addr = http_socket.accept()
            session = Session(c_conn, c_addr)
            asyncio.run(session.resolve())
