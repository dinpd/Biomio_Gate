__author__ = 'alexchmykhalo'

import tornado.gen


PICTURE_PATH_BAD_1 = "/home/alexchmykhalo/ios_screens/algorithms/yaleB11_P00A+000E+00.png"
DATA_PATH_BAD_2 = "/home/alexchmykhalo/ios_screens/algorithms/data.json"
PICTURE_PATH_GOOD_3 = "/home/alexchmykhalo/ios_screens/algorithms/yaleB11_P00A+000E+00.pgm"
FOLDER_DB_PATH_GOOD_3 = "/home/alexchmykhalo/ios_screens/algorithms"

from biomio.algorithms.algo_jobs import verification_job
import json
import os


def loadSources(path):
    if len(path):
        if not os.path.exists(path):
            return dict()
        with open(path, "r") as data_file:
            source = json.load(data_file)
            return source
    return dict()


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
    def probe(self, type, data, callback):
        settings = dict()
        settings['algoID'] = "001002"
        settings['userID'] = "0000000000000"
        settings['data'] = PICTURE_PATH_GOOD_3
        settings['database'] = loadSources(FOLDER_DB_PATH_GOOD_3 + "/data" + settings['algoID'] + ".json")
        verification_job(**settings)
        callback(True)
        pass
