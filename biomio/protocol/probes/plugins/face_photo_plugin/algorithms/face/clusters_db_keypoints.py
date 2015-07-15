from __future__ import absolute_import

import itertools
import numpy
import logger
from biomio.algorithms.algorithms.features.matchers import Matcher, BruteForceMatcherType
from biomio.protocol.probes.plugins.face_photo_plugin.algorithms.face.clusters_keypoints import ClustersMatchingDetector
from biomio.algorithms.algorithms.cvtools.types import listToNumpy_ndarray, numpy_ndarrayToList
from biomio.algorithms.algorithms.recognition.keypoints import verifying


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
        self._database = [dict() for _ in source.keys()]
        for c_num, item in source.iteritems():
            item_data = [[] for _ in item.keys()]
            for d_num, cluster in item.iteritems():
                desc = [[] for _ in cluster.keys()]
                for e_num, descriptor in cluster.iteritems():
                    desc[int(e_num)] = listToNumpy_ndarray(descriptor)
                item_data[int(d_num)] = desc
            obj = dict()
            obj["clusters"] = item_data
            self._database[int(c_num) - 1] = obj

    def exportSources(self):
        data = self.exportSources_Database()
        source = dict()
        if len(data.keys()) > 0:
            source['data'] = data
            source['threshold'] = self._prob
        return source

    def exportSources_Database(self):
        etalon = dict()
        for i, data in enumerate(self._database):
            elements = dict()
            for index, cluster in enumerate(data["clusters"]):
                desc = dict()
                if cluster is not None:
                    for indx, c in enumerate(cluster):
                        desc[indx] = numpy_ndarrayToList(c)
                elements[str(index)] = desc
            etalon[str(i)] = elements
        return etalon

    @verifying
    def verify(self, data):
        matcher = Matcher(BruteForceMatcherType)
        gres = []
        for d in self._database:
            res = []
            for i, source in enumerate(d['clusters']):
                test = data['clusters'][i]
                if (test is None) or (source is None) or (len(test) == 0) or (len(source) == 0):
                    logger.algo_logger.debug("Cluster #" + str(i + 1) + ": Invalid")
                else:
                    matches = matcher.knnMatch(listToNumpy_ndarray(test, numpy.uint8),
                                               listToNumpy_ndarray(source, numpy.uint8), k=1)
                    ms = sum(itertools.imap(
                        lambda v: len(v) >= 1 and v[0].distance < self.kodsettings.neighbours_distance,
                        matches)
                    )
                    prob = ms / (1.0 * len(matches))
                    res.append(prob * 100)
                    logger.algo_logger.debug("Cluster #" + str(i + 1) + " (Size: " + str(len(source)) + "): "
                                             + str(prob * 100) + "%")
            suma = sum(res)
            logger.algo_logger.debug("Total for image: " + str(suma / len(res)))
            gres.append(suma / len(res))
        s = sum(gres)
        logger.algo_logger.debug("Total: " + str(s / len(gres)))
        return s / len(gres)
