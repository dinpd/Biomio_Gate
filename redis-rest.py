import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.gen
from biomio.protocol.data_stores.base_data_store import BaseDataStore

from biomio.protocol.data_stores.session_data_store import SessionDataStore
from biomio.protocol.storage.redisstore import RedisStore
from biomio.protocol.storage.userinfodatastore import UserInfoDataStore
from biomio.protocol.data_stores.user_data_store import UserDataStore

import ast
import greenado

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

@greenado.generator
def get_user_data_helper(user_id, key=None):
    value = None

    app_data = yield tornado.gen.Task(UserDataStore.instance().get_data, str(user_id))

    if app_data is None:
        app_data = {}

    if key is not None:
        value = app_data.get(key, None)

    raise tornado.gen.Return(value=value)


def get_name():
    return get_user_data_helper(user_id='userid', key='name')


class RQTest(tornado.web.RequestHandler):

    @greenado.groutine
    def post(self):
        UserDataStore.instance().store_data(user_id='userid', name='datavalue')
        BaseDataStore.instance().delete_custom_redis_data(UserDataStore.get_data_key('userid'))

        name = get_name()
        print " NAME : ", name

        # UserDataStore.instance().get_data(user_id='userid', callback=test_get_result)


def test_get_result(result=None):
    print 'Result of the GET method - %s' % result


application = tornado.web.Application([
    (r"/redis", RQTest)
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
