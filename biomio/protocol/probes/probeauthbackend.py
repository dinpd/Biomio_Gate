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

    def _run_face_recognition(self, data):
        result = False
        for sample in data:
            #TODO: run job instead of direct call
            #TODO: create temporary folder and store picture

            # Create temporary file
            file_path = 'photo.pgm'
            photo_data = binascii.a2b_base64(str(sample))
            with open(file_path, 'wb') as f:
                f.write(photo_data)

            settings = dict()
            settings['algoID'] = "001002"
            settings['userID'] = "0000000000000"
            settings['data'] = PICTURE_PATH_GOOD_3
            settings['database'] = loadSources(FOLDER_DB_PATH_GOOD_3 + "/data" + settings['algoID'] + ".json")
            sample_result = verification_job(**settings)
            #TODO: proper handling of sample results
            result = result or sample_result

            # Remove temporary file
            os.remove(file_path)
        return result

    @tornado.gen.engine
    def probe(self, type, data, callback):
        logger.debug('Processing probe (%s)...' % type)

        result = False
        #TODO: use resourceitem types instead
        # if type == "fp-scanner":
        if type == "touchIdSamples":
            for sample in data:
                touch_id_result = (str(sample).lower() == 'true')
                result = result or touch_id_result
        # elif type == "face-photo":
        elif type == "imageSamples":
            result = self._run_face_recognition(data=data)
        else:
            logger.error('Unknown probe type %s' % type)

        callback(result)
        pass
