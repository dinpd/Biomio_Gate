import tornado.escape
import tornado.ioloop
import tornado.web
from biomio.protocol.data_stores.base_data_store import BaseDataStore

from biomio.protocol.data_stores.session_data_store import SessionDataStore
from biomio.protocol.storage.redisstore import RedisStore
from biomio.protocol.storage.userinfodatastore import UserInfoDataStore


class RedisHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            email = tornado.escape.url_unescape(self.get_argument('email'))
            user_id = UserInfoDataStore.instance().get_user_id_by_email(email=email)
            user_data = UserInfoDataStore.instance().get_user_data_by_id(user_id=user_id,
                                                                         key=UserInfoDataStore.USER_DATA_KEY)
            try:
                del user_data[email]
            except KeyError:
                pass

            UserInfoDataStore.instance().store_user_data(user_id=user_id, user_data=user_data)

        except Exception as e:
            email = str(e)
        self.write(email)


class RQTest(tornado.web.RequestHandler):
    def post(self):
        SessionDataStore.instance().store_data(refresh_token='test_refresh_token', ttl=10000,
                                               state='Test Refresh State')
        BaseDataStore.instance().delete_custom_redis_data('token:test_refresh_token')
        SessionDataStore.instance().get_data('test_refresh_token', test_get_result)

        RedisStore.instance()


def test_get_result(result):
    print 'Result of the GET method - %s' % result


application = tornado.web.Application([
    (r"/redis", RQTest)
])

if __name__ == "__main__":
    application.listen(8880)
    tornado.ioloop.IOLoop.instance().start()
