from email.utils import formatdate

from utils import HttpRespBuilder, HttpRequest
from utils import interpret
from utils import logger

class TopicHandler:

    def __init__(self, topics):
        self.topics = topics

    def __on_post(self, path: str):
        self.topics[path] = MessageHandler(path)
        return HttpRespBuilder(200) \
            .add_header('Server', 'ProChat') \
            .add_header('Content-Type', 'text/plain; charset=utf-8') \
            .add_header('Access-Control-Allow-Origin', '*') \
            .add_header('Date', formatdate(timeval=None, localtime=False, usegmt=True)) \
            .add_to_body(path) \
            .compile()

    def __on_delete(self, path: str):
        return HttpRespBuilder(200) \
            .add_header('Server', 'ProChat') \
            .add_header('Content-Type', 'text/plain; charset=utf-8') \
            .add_header('Access-Control-Allow-Origin', '*') \
            .add_header('Date', formatdate(timeval=None, localtime=False, usegmt=True)) \
            .add_to_body(path) \
            .compile()

    def __on_get(self):
        topics = ""
        for k in self.topics.keys():
            topics += k + " "
        return HttpRespBuilder(200) \
            .add_header('Server', 'ProChat') \
            .add_header('Content-Type', 'text/plain; charset=utf-8') \
            .add_header('Access-Control-Allow-Origin', '*') \
            .add_header('Date', formatdate(timeval=None, localtime=False, usegmt=True)) \
            .add_to_body(topics) \
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
        msg = ""
        if self.msg_queue:
            msg = self.msg_queue.pop(0)
        return HttpRespBuilder(200) \
            .add_header('Server', 'ProChat') \
            .add_header('Content-Type', 'text/plain; charset=utf-8') \
            .add_header('Access-Control-Allow-Origin', '*') \
            .add_header('Date', formatdate(timeval=None, localtime=False, usegmt=True)) \
            .add_to_body(msg) \
            .compile()

    @logger
    def __on_post(self, code):
        result = interpret(code)
        self.msg_queue.append(result)
        return HttpRespBuilder(200) \
            .add_header('Server', 'ProChat') \
            .add_header('Content-Type', 'text/plain; charset=utf-8') \
            .add_header('Access-Control-Allow-Origin', '*') \
            .add_header('Date', formatdate(timeval=None, localtime=False, usegmt=True)) \
            .add_to_body(str(result)) \
            .compile()

    def handle(self, req: HttpRequest):
        if req.method == 'POST':
            code = req.body
            return self.__on_post(code)
        if req.method == 'GET':
            return self.__on_get()