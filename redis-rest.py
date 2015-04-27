import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.gen

from biomio.algorithms.algo_job_processor import run_algo_job
from biomio.algorithms.algo_jobs import verification_job
from biomio.protocol.storage.probe_results_listener import ProbeResultsListener
from biomio.protocol.data_stores.user_data_store import UserDataStore

import greenado
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

        DEVICE_TOKEN_TEST = 'db740759eed8b161e5f703e360734cf2755b83872a72e8a7110a157247db001d'

        send_push_notification(device_token=DEVICE_TOKEN_TEST, message='TEst', use_sandbox=True)


def test_get_result(result=None):
    print 'Result of the GET method - %s' % result


application = tornado.web.Application([
    (r"/redis", RQTest)
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
