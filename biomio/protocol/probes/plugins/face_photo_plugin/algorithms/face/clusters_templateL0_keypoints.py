from __future__ import absolute_import
from biomio.protocol.probes.plugins.face_photo_plugin.algorithms.face.clusters_keypoints import ClustersMatchingDetector
from biomio.algorithms.cvtools.types import listToNumpy_ndarray, numpy_ndarrayToList
from biomio.algorithms.recognition.estimation import ClusterL0Estimation
from biomio.algorithms.recognition.keypoints import verifying
import logger
import sys


class ClustersTemplateL0MatchingDetector(ClustersMatchingDetector):
    def __init__(self):
        ClustersMatchingDetector.__init__(self)

    def threshold(self):
        return self._coff * self._prob

    def update_hash(self, data):
        del data['keypoints']
        del data['descriptors']
        self._database.append(data)
        self.update_hash_templateL0(data)

    def update_hash_templateL0(self, data):
        estimation = ClusterL0Estimation(self.kodsettings.detector_type, 3)
        self._etalon = estimation.estimate_training(data['clusters'], self._etalon)

    def update_database(self):
        try:
            self._prob = 100
            for data in self._database:
                temp_prob = self.verify_template_L0(data)
                if temp_prob < self._prob:
                    self._prob = temp_prob
            logger.algo_logger.debug('Database threshold: %s' % self._prob)
        except Exception as e:
            logger.algo_logger.exception(e)
            self._prob = sys.maxint
        return self._prob > self.kodsettings.probability

    def importSources(self, source):
        logger.algo_logger.debug("Database loading started...")
        self.importSources_L0Template(source.get('data', dict()))
        self._prob = source.get('threshold', 100)
        logger.algo_logger.info('Dynamic threshold: %f' % self._prob)
        logger.algo_logger.debug("Database loading finished.")

    def importSources_L0Template(self, source):

        def _values(d, key=None):
            l = sorted(d, key=key)
            for e in l:
                yield d[e]

        self._etalon = [
            [
                listToNumpy_ndarray(descriptor) for descriptor in _values(cluster)
            ] for cluster in _values(source, key=int)
        ]

    def exportSources(self):
        data = self.exportSources_L0Template()
        if len(data.keys()) > 0:
            return {
                'data': data,
                'threshold': self._prob
            }
        else:
            return {}

    def exportSources_L0Template(self):
        return {
            str(index): {} if cluster is None else {
                i: numpy_ndarrayToList(descriptor) for i, descriptor in enumerate(cluster)
                } for index, cluster in enumerate(self._etalon)
            }

    @verifying
    def verify(self, data):
        return self.verify_template_L0(data)

    def verify_template_L0(self, data):
        estimation = ClusterL0Estimation(self.kodsettings.detector_type, 2)
        logger.algo_logger.debug("Image: " + data['path'])
        return estimation.estimate_verification(data['clusters'], self._etalon)
