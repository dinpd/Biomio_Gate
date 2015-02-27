from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
from biomio.protocol.storage.userinfodatastore import UserInfoDataStore
 
class RedisHandler(tornado.web.RequestHandler):
    def post(self):
        email = tornado.escape.url_unescape(self.get_argument('email'))
        print email
        email = 'andriy.lobashchuk@vakoms.com.ua'
        user_id = UserInfoDataStore.instance().get_user_id_by_email(email=email)
        print user_id
        user_data = UserInfoDataStore.instance().get_user_data_by_id(user_id=user_id,
                                                                     key=UserInfoDataStore.USER_DATA_KEY)
        print 'user data: ', user_data
        del user_data[email]
        print user_data
        UserInfoDataStore.instance().store_user_data(user_id=user_id, user_data=user_data)
        self.write(email)
  
application = tornado.web.Application([
    (r"/redis", RedisHandler)
])
 
if __name__ == "__main__":
    application.listen(8880)
    tornado.ioloop.IOLoop.instance().start()
