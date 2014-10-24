#!/usr/bin/env python

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop


from biomio.protocol.message import BiomioClientMessageOld, BiomioServerMessageOld
from biomio.protocol.engine import BiomioProtocol

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.biomio_protocol = BiomioProtocol()
        pass

    def on_message(self, message_string):
        print 'Got message "%s" ' % message_string
        message = BiomioClientMessageOld.from_string(message_string)
        answer = self.biomio_protocol.process_next(message)
        self.write_message(answer.dumps())

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