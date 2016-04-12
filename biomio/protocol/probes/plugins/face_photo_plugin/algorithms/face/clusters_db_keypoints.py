from biomio.protocol.probes.plugins.face_photo_plugin.algorithms.face.clusters_keypoints import ClustersMatchingDetector
from biomio.algorithms.cvtools.types import listToNumpy_ndarray, numpy_ndarrayToList
from biomio.algorithms.recognition.estimation import ClusterDBEstimation
from biomio.algorithms.recognition.keypoints import verifying
from biomio.algorithms.logger import logger


class ClustersDBMatchingDetector(ClustersMatchingDetector):
    def __init__(self):
        ClustersMatchingDetector.__init__(self)

    def update_hash(self, data):
        del data['keypoints']
        del data['descriptors']
        self._database.append(data)

    def importSources(self, source):
        self._etalon = []
        logger.debug("Database loading started...")
        self.importSources_Database(source.get('data', dict()))
        self._prob = source.get('threshold', 100)
        logger.algo_logger.debug("Database loading finished.")

    def importSources_Database(self, source):

        def _values(d, key=None):
            l = sorted(d, key=key)
            for e in l:
                yield d[e]

        self._database = [
            {
                'clusters': [
                    [
                        listToNumpy_ndarray(descriptor) for descriptor in _values(cluster)
                    ] for cluster in _values(item, key=int)
                ]
            } for item in _values(source)
        ]

    def exportSources(self):
        data = self.exportSources_Database()
        if len(data.keys()) > 0:
            return {
                'data': data,
                'threshold': self._prob
            }
        else:
            return {}

    def exportSources_Database(self):
        return {
            str(i): {
                str(index): {
                    indx: numpy_ndarrayToList(c) for (indx, c) in enumerate(cluster)
                    } for (index, cluster) in enumerate(data['clusters']) if cluster is not None
                } for (i, data) in enumerate(self._database)
            }

    @verifying
    def verify(self, data):
        estimation = ClusterDBEstimation(self.kodsettings.detector_type,
                                         self.kodsettings.neighbours_distance)
        return estimation.estimate_verification(data, self._database)
