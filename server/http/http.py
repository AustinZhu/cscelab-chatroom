import asyncio
import logging
import socket

from .router import Router


class Session:
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        logging.info(f"Coming Request from {addr}")


class HttpServer:
    HTTP_HOST = "127.0.0.1"
    HTTP_PORT = 8080

    @classmethod
    async def serve(cls):
        http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        http_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        http_socket.bind((cls.HTTP_HOST, cls.HTTP_PORT))
        logging.info(f"Server started on port {cls.HTTP_PORT}")
        http_socket.listen(5)
        http_socket.setblocking(False)

        loop = asyncio.get_event_loop()
        router = Router()
        while True:
            c_conn, c_addr = await loop.sock_accept(http_socket)
            session = Session(c_conn, c_addr)
            loop.create_task(router.resolve(session))
