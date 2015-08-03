from __future__ import absolute_import
from biomio.protocol.probes.plugins.face_photo_plugin.algorithms.face.clusters_keypoints import ClustersMatchingDetector
from biomio.algorithms.algorithms.cvtools.types import listToNumpy_ndarray, numpy_ndarrayToList
from biomio.algorithms.algorithms.features import matcherForDetector, dtypeForDetector
from biomio.algorithms.algorithms.recognition.keypoints import verifying
from biomio.algorithms.algorithms.features.matchers import Matcher
import itertools
import logger


class ClustersDBMatchingDetector(ClustersMatchingDetector):
    def __init__(self):
        ClustersMatchingDetector.__init__(self)

    def update_hash(self, data):
        del data['keypoints']
        del data['descriptors']
        self._database.append(data)

    def importSources(self, source):
        self._etalon = []
        logger.algo_logger.debug("Database loading started...")
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

    def _probability(self, matcher, source, test):
        dtype = dtypeForDetector(self.kodsettings.detector_type)
        matches = matcher.knnMatch(listToNumpy_ndarray(test, dtype),
                                   listToNumpy_ndarray(source, dtype), k=1)
        ms = sum(
            itertools.imap(
                lambda v: len(v) >= 1 and v[0].distance < self.kodsettings.neighbours_distance, matches
            )
        )
        return ms / (1.0 * len(matches))

    @verifying
    def verify(self, data):
        matcher = Matcher(matcherForDetector(self.kodsettings.detector_type))
        tprob = 0
        for d in self._database:
            prob = [0, 0]
            for i, source in enumerate(d['clusters']):
                test = data['clusters'][i]
                if (test is None) or (source is None) or (len(test) == 0) or (len(source) == 0):
                    logger.algo_logger.debug("Cluster #%d: Invalid" % (i + 1))
                else:
                    _prob = 100 * self._probability(matcher, source, test)
                    prob[0] += _prob
                    prob[1] += 1
                    logger.algo_logger.debug("Cluster #%d (Size: %d): %f%%" % (i + 1, len(source), _prob))
            logger.algo_logger.debug("Total for image: %f%%" % (prob[0]/prob[1]))
            tprob += (prob[0] / prob[1])
        logger.algo_logger.debug("Total: %d%%" % (tprob / len(self._database)))
        return tprob / len(self._database)
