#!/usr/bin/env python

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop


from biomio.protocol.message import BiomioMessage
from biomio.protocol.engine import BiomioProtocol

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.biomio_protocol = BiomioProtocol(close_callback=self.close, send_callback=self.write_message)

    def on_message(self, message_string):
        message = BiomioMessage.fromJson(message_string)
        self.biomio_protocol.process_next(message)

    def on_close(self):
        pass


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/websocket', WebSocketHandler)
        ]

        tornado.web.Application.__init__(self, handlers)


def run_tornado():
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    print 'Running tornado server...'
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    # Run tornado application
    run_tornado()