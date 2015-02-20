#!/usr/bin/env python

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.gen

from biomio.protocol.engine import BiomioProtocol
from biomio.protocol.settings import settings
from biomio.protocol.connectionhandler import ConnectionTimeoutHandler

import logging
logger = logging.getLogger(__name__)

ssl_options = {
        "certfile": "server.crt",
        "keyfile": "server.key"
}


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    
    def check_origin(self, origin):
        return True

    def open(self):
        self.biomio_protocol = BiomioProtocol(
            close_callback=self.close,
            send_callback=self.write_message,
            start_connection_timer_callback=self.start_connection_timer,
            stop_connection_timer_callback=self.stop_connection_timer,
            check_connected_callback=self.check_connected
        )
        self.start_connection_timer()

    def on_message(self, message_string):
        self.biomio_protocol.process_next(message_string)

    def on_close(self):
        ConnectionTimeoutHandler.instance().stop_connection_timer(connection=self)
        self.biomio_protocol.connection_closed()

    def stop_connection_timer(self):
        ConnectionTimeoutHandler.instance().stop_connection_timer(connection=self)

    def start_connection_timer(self):
        ConnectionTimeoutHandler.instance().start_connection_timer(connection=self, timeout_callback=self.on_connection_timeout)

    def on_connection_timeout(self):
        logger.debug('Connection timeout')
        self.biomio_protocol.close_connection(status_message='Connection timeout')


    def check_connected(self):
        return bool(self.ws_connection)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/websocket', WebSocketHandler)
        ]

        tornado.web.Application.__init__(self, handlers)

def run_tornado():
    app = Application()
    server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_options)
    logger.info('Running tornado server...')
    server.listen(settings.port)
    tornado.ioloop.IOLoop.instance().start()

from biomio.protocol.message import BiomioMessageBuilder

# import python_jsonschema_objects as pjs
# from biomio.protocol.schema import BIOMIO_protocol_json_schema

if __name__ == '__main__':

    logging.basicConfig(
        format='%(levelname)-8s [%(asctime)s] %(message)s',
        level=logging.DEBUG
    )

    # msg = {
    #   "msg" : {
    #     "oid" : "probe",
    #     "probeId" : 0,
    #     "probeData": {"oid": "imageSamples", "samples": ["enhjYnh6YmN4emJtY2J4em1jYmFzamdhanNkZ2pzYXZkc2EgZG1hc21kbmI=", "enhjYnh6YmN4emJtY2J4em1jYmFzamdhanNkZ2pzYXZkc2EgZG1hc21kbmI="]}
    #         # {"oid": "touchIdSamples", "samples": ["True", "False"]}
    #   },
    #   "header" : {
    #     "id" : "0UMhRvDTEOEw93x8SROygESdI",
    #     "osId" : "iOS_8.1",
    #     "devId" : "021DD1E2-5D5A-423B-9B64-37FDCD536FE8",
    #     "appId" : "probe_lIErKOvKhhYcSt9esg7eXatmY",
    #     "oid" : "clientHeader",
    #     "protoVer" : "1.0",
    #     "seq" : 24
    #   }
    # }
    #
    # builder = pjs.ObjectBuilder(BIOMIO_protocol_json_schema)
    # ns = builder.build_classes()
    # biomio_message = ns.BiomioSchema(**msg)
    # print biomio_message.serialize()

    # Run tornado application
    run_tornado()
