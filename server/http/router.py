import asyncio

from server.http.handler import TopicHandler, MessageHandler
from server.http.utils import parse_http_req


class Router:
    def __init__(self):
        self.topics = {
            "/topic": TopicHandler()
        }

    async def resolve(self, session):
        loop = asyncio.get_event_loop()
        payload = await loop.sock_recv(session.sock, 1024)

        req = parse_http_req(payload.decode('utf-8'))
        handler = self.topics[req.path]
        resp = handler.handle(req)

        await loop.sock_sendall(session.sock, resp)
        session.sock.close()