from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
from biomio.protocol.storage.userinfodatastore import UserInfoDataStore
 
class RedisHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('ok')
  
application = tornado.web.Application([
    (r"/paypal", RedisHandler)
])
 
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
