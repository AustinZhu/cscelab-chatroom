import json
from email.utils import formatdate

from server.http.utils import HttpRespBuilder, HttpRequest
from server.http.utils import interpret
from server.http.utils import logger

class TopicHandler:

    def __init__(self):
        self.topics = dict()

    def __on_post(self, name: str):
        self.topics[name] = MessageHandler(name)
        return HttpRespBuilder(200) \
            .add_header('Server', 'ProChat') \
            .add_header('Content-Type', 'text/html; charset=utf-8') \
            .add_header('Access-Control-Allow-Origin', '*') \
            .add_header('Date', formatdate(timeval=None, localtime=False, usegmt=True)) \
            .add_to_body(f"<html><body>Created topic: {name}</body></html>") \
            .compile()

    def __on_delete(self, name: str):
        return HttpRespBuilder(200) \
            .add_header('Server', 'ProChat') \
            .add_header('Content-Type', 'text/html; charset=utf-8') \
            .add_header('Access-Control-Allow-Origin', '*') \
            .add_header('Date', formatdate(timeval=None, localtime=False, usegmt=True)) \
            .add_to_body(f"<html><body>Deleted topic: {name}</body></html>") \
            .compile()

    def __on_get(self):
        topics = list(self.topics.keys())
        return HttpRespBuilder(200) \
            .add_header('Server', 'ProChat') \
            .add_header('Content-Type', 'text/html; charset=utf-8') \
            .add_header('Access-Control-Allow-Origin', '*') \
            .add_header('Date', formatdate(timeval=None, localtime=False, usegmt=True)) \
            .add_to_body(f"<html><body>Topics:<br>{topics}</body></html>") \
            .compile()

    def handle(self, req: HttpRequest):
        if req.method == 'POST':
            return self.__on_post(req.body)
        if req.method == 'GET':
            return self.__on_get()
        if req.method == 'DELETE':
            return self.__on_delete(req.body)

class MessageHandler:

    def __init__(self, topic):
        self.topic = topic
        self.msg_queue = []
        self.sessions = []

    @logger
    def __on_get(self):
        msg = self.msg_queue.pop(0)
        return HttpRespBuilder(200) \
            .add_header('Server', 'ProChat') \
            .add_header('Content-Type', 'text/html; charset=utf-8') \
            .add_header('Access-Control-Allow-Origin', '*') \
            .add_header('Date', formatdate(timeval=None, localtime=False, usegmt=True)) \
            .add_to_body(f"<html><body>{msg}</body></html>") \
            .compile()

    @logger
    def __on_post(self, code):
        result = interpret(code)
        return HttpRespBuilder(200) \
            .add_header('Server', 'ProChat') \
            .add_header('Content-Type', 'text/html; charset=utf-8') \
            .add_header('Access-Control-Allow-Origin', '*') \
            .add_header('Date', formatdate(timeval=None, localtime=False, usegmt=True)) \
            .add_to_body(f"<html><body>Your message is:<br>{str(result)}</body></html>") \
            .compile()

    def handler(self, req: HttpRequest):
        if req.method == 'POST':
            code = json.loads(req.body)["code"]
            return self.__on_post(code)
        if req.method == 'GET':
            return self.__on_get()