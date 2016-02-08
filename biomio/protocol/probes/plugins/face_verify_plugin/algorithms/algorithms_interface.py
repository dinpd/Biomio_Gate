from __future__ import absolute_import
import json
import os

import logger
from biomio.algorithms.imgobj import loadImageObject
from biomio.protocol.probes.plugins.face_verify_plugin.algorithms.face import (
    getClustersMatchingDetectorWithoutTemplate,
    getClustersMatchingDetectorWithL0Template,
    getClustersMatchingDetectorWithL1Template
)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
SETTINGS_DIR = os.path.join(APP_ROOT, 'settings')

class AlgorithmsInterface:
    def __init__(self):
        pass

    @staticmethod
    def getAlgorithm(algoID):
        """
        Return algorithm object by algorithm ID algoID.

        :param algoID: Unique algorithm identificator
                001     - Verification algorithms
                00101   - Clustering Matching Verification algorithm
                            without creating template
                        001011 - ... based on openCV BRISK Features Detector
                        001012 - ... based on openCV ORB Features Detector
                        001013 - ... based on openCV SURF Features Detector
                        001014 - ... based on mahotas SURF Features Detector
                00102   - Clustering Matching Verification algorithm
                            with creating L0-layer template
                        001021 - ... based on openCV BRISK Features Detector
                        001022 - ... based on openCV ORB Features Detector    (Default)
                        001023 - ... based on openCV SURF Features Detector
                        001024 - ... based on mahotas SURF Features Detector
                00103   - Clustering Matching Verification algorithm
                            with creating L1-layer template
                        001031 - ... based on openCV BRISK Features Detector
                        001032 - ... based on openCV ORB Features Detector
                        001033 - ... based on openCV SURF Features Detector
                        001034 - ... based on mahotas SURF Features Detector
                002     - Identification algorithms
        :return: Algorithm object instance
        """
        if algoID and len(algoID) == 6:
            algorithms = {"001011": (getClustersMatchingDetectorWithoutTemplate, 'BRISK'),
                          "001012": (getClustersMatchingDetectorWithoutTemplate, 'ORB'),
                          "001013": (getClustersMatchingDetectorWithoutTemplate, 'SURF'),
                          "001014": (getClustersMatchingDetectorWithoutTemplate, 'mSURF'),
                          "001021": (getClustersMatchingDetectorWithL0Template, 'BRISK'),
                          "001022": (getClustersMatchingDetectorWithL0Template, 'ORB'),
                          "001023": (getClustersMatchingDetectorWithL0Template, 'SURF'),
                          "001024": (getClustersMatchingDetectorWithL0Template, 'mSURF'),
                          "001031": (getClustersMatchingDetectorWithL1Template, 'BRISK'),
                          "001032": (getClustersMatchingDetectorWithL1Template, 'ORB'),
                          "001033": (getClustersMatchingDetectorWithL1Template, 'SURF'),
                          "001034": (getClustersMatchingDetectorWithL1Template, 'mSURF')
                          }
            if algorithms.keys().__contains__(algoID):
                return algorithms[algoID][0](), algorithms[algoID][1]
        return None, ''

    @staticmethod
    def verification(**kwargs):
        logger.algo_logger.info('###################################')
        logger.algo_logger.info('Verification Process')
        logger.algo_logger.info('Starting...')
        record = dict()
        if not kwargs:
            record['status'] = "error"
            record['type'] = "Algorithm settings are empty"
            logger.algo_logger.info('Error::%s' % record['type'])
            return record
        if not kwargs.get('userID', None):
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['param'] = 'userID'
            details['message'] = "The user ID is empty."
            record['details'] = details
            logger.algo_logger.info('Error::%s::%s' % (record['type'], details['message']))
            return record
        logger.algo_logger.info('User ID: %s' % kwargs['userID'])
        if not kwargs.get('algoID', None):
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['param'] = 'algoID'
            details['message'] = "The algorithm ID is empty."
            record['details'] = details
            logger.algo_logger.info('Error::%s::%s' % (record['type'], details['message']))
            return record
        logger.algo_logger.info('Algorithm ID: %s' % kwargs['algoID'])
        algorithm, prefix = AlgorithmsInterface.getAlgorithm(kwargs['algoID'])
        if not algorithm:
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['param'] = 'algoID'
            details['message'] = "Such algorithm ID %s doesn't exist." % kwargs['algoID']
            record['details'] = details
            logger.algo_logger.info('Error::%s::%s' % (record['type'], details['message']))
            return record
        if not kwargs.get('data', None):
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['param'] = 'data'
            details['message'] = "The data source is empty."
            record['details'] = details
            logger.algo_logger.info('Error::%s::%s' % (record['type'], details['message']))
            return record
        if not algorithm.importSettings(AlgorithmsInterface.loadSettings(kwargs['algoID'], prefix)):
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['message'] = "Cannot loading settings."
            record['details'] = details
            logger.algo_logger.info('Error::%s::%s' % (record['type'], details['message']))
            return record
        if not kwargs.get('action', None):
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['param'] = 'action'
            details['message'] = "The action parameter is empty."
            record['details'] = details
            logger.algo_logger.info('Error::%s::%s' % (record['type'], details['message']))
            return record
        if kwargs['action'] == 'education':
            if kwargs.get('database', None):
                algorithm.importSources(kwargs['database'])
            img_list = []
            for image_path in kwargs['data']:
                imgobj = loadImageObject(image_path)
                if not imgobj:
                    record['status'] = "error"
                    record['type'] = "Invalid algorithm settings"
                    details = dict()
                    details['param'] = 'data'
                    details['message'] = "Such data %s doesn't exists." % image_path
                    record['details'] = details
                    logger.algo_logger.info('Error::%s::%s' % (record['type'], details['message']))
                    return record
                img_list.append(imgobj)
            count = algorithm.addSources(img_list)
            result_list = []
            if count < len(kwargs['data']) / 2.0:
                record['status'] = "error"
                record['type'] = "Internal Training Error"
                details = dict()
                details['param'] = 'data'
                details['message'] = "Problem with training images detection."
                record['details'] = details
                logger.algo_logger.info("Internal Training Error::Problem with training images detection.")
                result_list.append(record)
            res = algorithm.update_database()
            if not res:
                record['status'] = "error"
                record['type'] = "Internal Training Error"
                details = dict()
                details['param'] = 'data'
                details['message'] = "Problem with updating of the dynamic threshold."
                record['details'] = details
                logger.algo_logger.info("Internal Training Error::Problem with updating of the dynamic threshold.")
                return record
            sources = algorithm.exportSources()
            res_record = dict()
            res_record['status'] = "update"
            res_record['algoID'] = kwargs['algoID']
            res_record['userID'] = kwargs['userID']
            res_record['database'] = sources
            logger.algo_logger.info('Status::The database updated.')
            if len(result_list) == 0:
                return res_record
            result_list.append(res_record)
            return result_list
        elif kwargs['action'] == 'verification':
            if not kwargs.get('database', None):
                record['status'] = "data_request"
                record['algoID'] = kwargs['algoID']
                record['userID'] = kwargs['userID']
                logger.algo_logger.info('Status::The request of the database.')
                return record
            algorithm.importSources(kwargs['database'])
            imgobj = loadImageObject(kwargs['data'])
            if not imgobj:
                record['status'] = "error"
                record['type'] = "Invalid algorithm settings"
                details = dict()
                details['param'] = 'data'
                details['message'] = "Such data %s doesn't exists." % kwargs['data']
                record['details'] = details
                logger.algo_logger.info('Error::%s::%s' % (record['type'], details['message']))
                return record
            result = algorithm.verify(imgobj)
            if not result and algorithm.last_error() != "":
                record['status'] = "error"
                record['type'] = "Internal algorithm error"
                details = dict()
                details['param'] = 'data'
                details['message'] = algorithm.last_error()
                record['details'] = details
                logger.algo_logger.info('Error::%s::%s' % (record['type'], details['message']))
                return record
            else:
                record['status'] = "result"
                record['result'] = result > algorithm.threshold()
                record['userID'] = kwargs['userID']
                logger.algo_logger.info('Result::%s' % str(record['result']))
                return record
        else:
            record['status'] = "error"
            record['type'] = "Invalid algorithm settings"
            details = dict()
            details['param'] = 'action'
            details['message'] = "Such action %s doesn't exists." % kwargs['action']
            record['details'] = details
            logger.algo_logger.info('Error::%s::%s' % (record['type'], details['message']))
            return record

    @staticmethod
    def loadSettings(algoID, prefix):
        settings_path = os.path.join(SETTINGS_DIR, prefix, "info" + algoID + ".json")
        if not os.path.exists(settings_path):
            return dict()
        with open(settings_path, "r") as data_file:
            source = json.load(data_file)
            return source
        return dict()
