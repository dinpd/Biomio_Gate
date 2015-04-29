import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.gen

from biomio.algorithms.algo_job_processor import run_algo_job
from biomio.algorithms.algo_jobs import verification_job
from biomio.constants import APPS_TABLE_CLASS_NAME
from biomio.protocol.data_stores.storage_jobs import get_probe_ids_by_user_email, get_extension_ids_by_probe_id
from biomio.protocol.data_stores.storage_jobs_processor import run_storage_job
from biomio.protocol.storage.probe_results_listener import ProbeResultsListener
from biomio.protocol.data_stores.user_data_store import UserDataStore

import greenado
from biomio.protocol.storage.redis_results_listener import RedisResultsListener
from biomio.utils.utils import send_push_notification


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

        # callback_code = ProbeResultsListener.instance().subscribe_callback(callback=test_get_result)
        # result_code = ProbeResultsListener.instance().activate_results_gatherer(results_count=5)
        # settings = dict(
        #     algoID="001002",
        #     userID="0000000000000"
        # )
        # for x in range(0, 5):
        #     run_algo_job(verification_job, image='', fingerprint='tetetet', settings=settings,
        #                  callback_code=callback_code, result_code=result_code)

        # Push Notifications test.

        # DEVICE_TOKEN_TEST = 'db740759eed8b161e5f703e360734cf2755b83872a72e8a7110a157247db001d'
        #
        # send_push_notification(device_token=DEVICE_TOKEN_TEST, message='TEst', use_sandbox=True)

        callback_code = RedisResultsListener.instance().subscribe_callback(callback=test_get_result)
        run_storage_job(get_probe_ids_by_user_email, table_class_name=APPS_TABLE_CLASS_NAME,
                        email='andriy.lobashchuk@vakoms.com.ua', callback_code=callback_code)

        probe_id = '88b960b1c9805fb586810f270def7378'
        callback_code = RedisResultsListener.instance().subscribe_callback(callback=test_get_result)
        run_storage_job(get_extension_ids_by_probe_id, table_class_name=APPS_TABLE_CLASS_NAME,
                        probe_id=probe_id, callback_code=callback_code)


def test_get_result(result=None):
    print 'Result of the GET method - %s' % result


application = tornado.web.Application([
    (r"/redis", RQTest)
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
