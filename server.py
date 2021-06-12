import asyncio

from server import HttpServer

if __name__ == '__main__':
    asyncio.run(HttpServer.serve())
