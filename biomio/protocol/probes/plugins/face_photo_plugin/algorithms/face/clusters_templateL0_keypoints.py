from biomio.protocol.probes.plugins.face_photo_plugin.algorithms.face.clusters_keypoints import ClustersMatchingDetector
from biomio.algorithms.recognition.estimation import SelfGraphEstimation, ClusterL0Estimation, DEFAULT_MODE
from biomio.algorithms.recognition.keypoints import verifying
from biomio.algorithms.logger import logger
import sys


class ClustersTemplateL0MatchingDetector(ClustersMatchingDetector):
    def __init__(self):
        ClustersMatchingDetector.__init__(self)
        self._w_clusters = None
        self._etalon = {}

    def threshold(self):
        return self._coff * self._prob

    def update_hash(self, data):
        del data['keypoints']
        del data['descriptors']
        self._database.append(data)
        self.update_hash_templateL0(data)

    def update_hash_templateL0(self, data):
        estimation = ClusterL0Estimation(self.kodsettings.detector_type, knn=3, max_distance=0.9,
                                         mode=DEFAULT_MODE)
        self._etalon = estimation.estimate_training(data['clusters'], self._etalon)
        # estimation = SelfGraphEstimation(self.kodsettings.detector_type, knn=3)
        # self._etalon = estimation.estimate_training(data, self._etalon)

    def update_database(self):
        try:
            self._prob = 100
            for data in self._database:
                temp_prob = self.verify_template_L0(data)
                if temp_prob < self._prob:
                    self._prob = temp_prob
            logger.debug('Database threshold: %s' % self._prob)
        except Exception as e:
            logger.exception(e)
            self._prob = sys.maxint
        return self._prob > self.kodsettings.probability

    def importSources(self, source):
        logger.debug("Database loading started...")
        self._etalon = SelfGraphEstimation.importDatabase(source.get('data', dict()))
        self._prob = source.get('threshold', 100)
        logger.info('Dynamic threshold: %f' % self._prob)
        logger.debug("Database loading finished.")

    @staticmethod
    def load_database(source):
        return {
            "template": SelfGraphEstimation.importDatabase(source.get('data', dict())),
            "threshold": source.get('threshold', 100)
        }

    def exportSources(self):
        data = SelfGraphEstimation.exportDatabase(self._etalon)
        if len(data.keys()) > 0:
            return {
                'data': data,
                'threshold': self._prob
            }
        else:
            return {}

    @verifying
    def verify(self, data):
        return self.verify_template_L0(data)

    def verify_template_L0(self, data):
        estimation = ClusterL0Estimation(self.kodsettings.detector_type, knn=2, max_distance=0.9,
                                         mode=DEFAULT_MODE)
        # estimation = SelfGraphEstimation(self.kodsettings.detector_type, knn=2)
        logger.debug("Image: " + data['path'])
        return estimation.estimate_verification(data['clusters'], self._etalon)
        # return estimation.estimate_verification(data, self._etalon)
