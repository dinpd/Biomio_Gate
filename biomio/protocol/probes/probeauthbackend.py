from biomio.algorithms.algo_job_processor import run_algo_job
from biomio.protocol.storage.probe_results_listener import ProbeResultsListener

__author__ = 'alexchmykhalo'

import tornado.gen


PICTURE_PATH_BAD_1 = "/home/alexchmykhalo/ios_screens/algorithms/yaleB11_P00A+000E+00.png"
DATA_PATH_BAD_2 = "/home/alexchmykhalo/ios_screens/algorithms/data.json"
PICTURE_PATH_GOOD_3 = "/home/alexchmykhalo/ios_screens/algorithms/yaleB11_P00A+000E+00.pgm"
FOLDER_DB_PATH_GOOD_3 = "/home/alexchmykhalo/ios_screens/algorithms"

from biomio.algorithms.algo_jobs import verification_job
import json
import os
import binascii


def loadSources(path):
    if len(path):
        if not os.path.exists(path):
            return dict()
        with open(path, "r") as data_file:
            source = json.load(data_file)
            return source
    return dict()

import logging
logger = logging.getLogger(__name__)

class ProbeAuthBackend:
    """
    Class ProbeAuthBackend provides implementation for singleton that manages
    asynchronous processing of different types of probes.
    """
    _instance = None

    @classmethod
    def instance(cls):
        """
        Provides singleton instance.
        :return: ProbeAuthBackend instance
        """
        if cls._instance is None:
            cls._instance = ProbeAuthBackend()

        return cls._instance

    def __init__(self):
        pass

    @tornado.gen.engine
    def probe(self, type, data, fingerprint=None, training=False, callback=None):
        logger.debug('Processing probe (%s)...' % type)

        result = False
        #TODO: use resourceitem types instead
        if type == "touchIdSamples":
            for sample in data:
                touch_id_result = (str(sample).lower() == 'true')
                result = result or touch_id_result
            callback(result)
        elif type == "imageSamples":
            callback_code = ProbeResultsListener.instance().subscribe_callback(callback=callback)
            run_algo_job(verification_job, callback_code=callback_code, data=data, fingerprint=fingerprint, education=training)
        else:
            logger.error('Unknown probe type %s' % type)
        pass
