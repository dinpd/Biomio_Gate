import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.gen
from biomio.constants import EMAILS_TABLE_CLASS_NAME
from biomio.mysql_storage.mysql_data_store import MySQLDataStore
from biomio.protocol.data_stores.application_data_store import ApplicationDataStore
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.protocol.data_stores.email_data_store import EmailDataStore

from biomio.protocol.data_stores.session_data_store import SessionDataStore
from biomio.protocol.storage.redisstore import RedisStore
from biomio.protocol.storage.userinfodatastore import UserInfoDataStore
from biomio.protocol.data_stores.user_data_store import UserDataStore
from biomio.protocol.crypt import Crypto

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
    app_data = yield tornado.gen.Task(UserDataStore.instance().get_data, str(user_id))

    value = None
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
        # SessionDataStore.instance().store_data(refresh_token='test_refresh_token', ttl=10000,
        # state='Test Refresh State')
        # BaseDataStore.instance().delete_custom_redis_data('token:test_refresh_token')
        # SessionDataStore.instance().get_data('test_refresh_token', test_get_result)
        # UserDataStore.instance().store_data(user_id='userid', name='datavalue')
        # BaseDataStore.instance().delete_custom_redis_data(UserDataStore.get_data_key('userid'))
        #
        # name = get_name()
        # print " NAME : ", name
        UserDataStore.instance().store_data(1)
        store_keywords = {ApplicationDataStore.APP_TYPE_ATTR: 'extension',
                          ApplicationDataStore.PUBLIC_KEY_ATTR: 'Test pub key',
                          ApplicationDataStore.USER_ATTR: 1}
        ApplicationDataStore.instance().store_data('test_app_id6', **store_keywords)
        store_keywords = {
            EmailDataStore.PASS_PHRASE_ATTR: 'test_pass_phrase',
            EmailDataStore.PUBLIC_PGP_KEY_ATTR: 'test_pub_pgp_key',
            EmailDataStore.PRIVATE_PGP_KEY_ATTR: None,
            EmailDataStore.USER_ATTR: 1
        }
        EmailDataStore.instance().store_data('test6@mail.com', **store_keywords)
        BaseDataStore.instance().delete_custom_lru_redis_data(ApplicationDataStore.get_data_key('test_app_id6'))
        BaseDataStore.instance().delete_custom_lru_redis_data(EmailDataStore.get_data_key('test6@mail.com'))
        ApplicationDataStore.instance().get_data(app_id='test_app_id6', callback=test_get_result)
        EmailDataStore.instance().get_data(email='test6@mail.com', callback=test_get_result)
        EmailDataStore.instance().select_data_by_ids(['test6@mail.com', 'test4@mail.com'], test_get_result)


def test_get_result(result=None):
    print 'Result of the GET method - %s' % result


application = tornado.web.Application([
    (r"/redis", RQTest)
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
