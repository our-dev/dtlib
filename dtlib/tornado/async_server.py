"""
替换掉tornado的ioloop
"""
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.netutil import add_accept_handler
from tornado.platform.asyncio import AsyncIOMainLoop
from tornado.tcpserver import TCPServer


class MyAsyncHttpServer(HTTPServer):
    """
    asyncio ioloop
    """

    def add_sockets(self, sockets):
        """
        重写sockets添加函数
        不使用tornado的默认的ioloop,
        而使用asyncio的ioloop实例
        :param sockets:
        :return:
        """
        AsyncIOMainLoop().install()
        if self.io_loop is None:
            self.io_loop = IOLoop.current()
            assert self.io_loop is not None, 'the io_loop shoud not be none'
            for sock in sockets:
                self._sockets[sock.fileno()] = sock
                add_accept_handler(sock, self._handle_connection,
                                   io_loop=self.io_loop)


class MyAsyncTCPServer(TCPServer):
    """
    使用
    asyncio ioloop
    替换掉tornado
    """

    def add_sockets(self, sockets):
        """
        重写sockets添加函数
        不使用tornado的默认的ioloop,
        而使用asyncio的ioloop实例
        :param sockets:
        :return:
        """
        AsyncIOMainLoop().install()
        # IOLoop.configure('tornado.platform.asyncio.AsyncIOMainLoop')
        if self.io_loop is None:
            self.io_loop = IOLoop.current()
            assert self.io_loop is not None, 'the io_loop shoud not be none'
        for sock in sockets:
            self._sockets[sock.fileno()] = sock
            add_accept_handler(sock, self._handle_connection,
                               io_loop=self.io_loop)
