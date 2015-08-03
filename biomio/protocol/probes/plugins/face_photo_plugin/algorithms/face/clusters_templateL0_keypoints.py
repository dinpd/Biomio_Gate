from __future__ import absolute_import
from biomio.protocol.probes.plugins.face_photo_plugin.algorithms.face.clusters_keypoints import ClustersMatchingDetector
from biomio.algorithms.algorithms.cvtools.types import listToNumpy_ndarray, numpy_ndarrayToList
from biomio.algorithms.algorithms.features import matcherForDetector, dtypeForDetector
from biomio.algorithms.algorithms.recognition.keypoints import verifying
from biomio.algorithms.algorithms.features.matchers import Matcher
import itertools
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
        if len(self._etalon) == 0:
            self._etalon = data['clusters']
        else:
            matcher = Matcher(matcherForDetector(self.kodsettings.detector_type))
            for index, et_cluster in enumerate(self._etalon):
                dt_cluster = data['clusters'][index]
                if et_cluster is None or len(et_cluster) == 0:
                    self._etalon[index] = et_cluster
                elif dt_cluster is None or len(dt_cluster) == 0:
                    self._etalon[index] = et_cluster
                else:
                    dtype = dtypeForDetector(self.kodsettings.detector_type)
                    matches1 = matcher.knnMatch(listToNumpy_ndarray(et_cluster, dtype),
                                                listToNumpy_ndarray(dt_cluster, dtype), k=3)
                    matches2 = matcher.knnMatch(listToNumpy_ndarray(dt_cluster, dtype),
                                                listToNumpy_ndarray(et_cluster, dtype), k=3)
                    good = list(itertools.chain.from_iterable(itertools.imap(
                        lambda(x, _): (et_cluster[x.queryIdx], dt_cluster[x.trainIdx]), itertools.ifilter(
                            lambda(m, n): m.queryIdx == n.trainIdx and m.trainIdx == n.queryIdx, itertools.product(
                                itertools.chain(*matches1), itertools.chain(*matches2)
                            )
                        )
                    )))
                    self._etalon[index] = listToNumpy_ndarray(good)

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
        matcher = Matcher(matcherForDetector(self.kodsettings.detector_type))
        prob = 0
        logger.algo_logger.debug("Image: " + data['path'])
        logger.algo_logger.debug("Template size: ")
        summ = sum(itertools.imap(lambda x: len(x) if x is not None else 0, self._etalon))
        for index, et_cluster in enumerate(self._etalon):
            dt_cluster = data['clusters'][index]
            if et_cluster is None:
                logger.algo_logger.debug("Cluster #" + str(index + 1) + ": " + str(-1)
                                         + " Invalid. (Weight: 0)")
                continue
            if dt_cluster is None:
                logger.algo_logger.debug("Cluster #" + str(index + 1) + ": " + str(len(self._etalon[index]))
                                         + " Positive: 0 Probability: 0 (Weight: " +
                                         str(len(et_cluster) / (1.0 * summ)) + ")")
                continue
            if len(et_cluster) > 0 and len(dt_cluster) > 0:
                dtype = dtypeForDetector(self.kodsettings.detector_type)
                matches1 = matcher.knnMatch(listToNumpy_ndarray(et_cluster, dtype),
                                            listToNumpy_ndarray(dt_cluster, dtype), k=2)
                matches2 = matcher.knnMatch(listToNumpy_ndarray(dt_cluster, dtype),
                                            listToNumpy_ndarray(et_cluster, dtype), k=2)
                ms = [
                    x for (x, _) in itertools.ifilter(
                        lambda(m, n): m.queryIdx == n.trainIdx and m.trainIdx == n.queryIdx, itertools.product(
                            itertools.chain(*matches1), itertools.chain(*matches2)
                        )
                    )
                ]
                val = (len(ms) / (1.0 * len(et_cluster))) * 100
                logger.algo_logger.debug("Cluster #" + str(index + 1) + ": " + str(len(et_cluster))
                                         + " Positive: " + str(len(ms)) + " Probability: " + str(val) +
                                         " (Weight: " + str(len(et_cluster) / (1.0 * summ)) + ")")
                prob += (len(et_cluster) / (1.0 * summ)) * val
            else:
                logger.algo_logger.debug("Cluster #" + str(index + 1) + ": " + str(len(et_cluster))
                                         + " Invalid.")
        logger.algo_logger.debug("Probability: " + str(prob))
        return prob
