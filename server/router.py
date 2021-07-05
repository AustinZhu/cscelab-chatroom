#ZHU Yiming; ZHENG Nianzhao; MAO Zhenyu

import asyncio

from handler import TopicHandler, MessageHandler
from utils import parse_http_req, HttpRespBuilder
from email.utils import formatdate


class Router:
    def __init__(self):
        self.topics = {}
        self.mainHandler = TopicHandler(self.topics)

    async def resolve(self, session):
        loop = asyncio.get_event_loop()
        payload = await loop.sock_recv(session.sock, 1024)

        req = parse_http_req(payload.decode('utf-8'))
        if req.path == "/topics":
            resp = self.mainHandler.handle(req)
        elif req.path not in self.topics:
            resp = HttpRespBuilder(404) \
               .add_header('Server', 'ProChat') \
               .add_header('Content-Type', 'text/html; charset=utf-8') \
               .add_header('Access-Control-Allow-Origin', '*') \
               .add_header('Date', formatdate(timeval=None, localtime=False, usegmt=True)) \
               .add_to_body(f"<html><body>No such topic</body></html>") \
               .compile()
        else:
            handler = self.topics.get(req.path)
            resp = handler.handle(req)

        await loop.sock_sendall(session.sock, resp)
        session.sock.close()
