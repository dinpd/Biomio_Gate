from biomio.algorithms.cascades.scripts_detectors import CascadesDetectionInterface
from biomio.algorithms.recognition.keypoints import KeypointsObjectDetector
from biomio.algorithms.cascades.detectors import OptimalROIDetectorSAoS
from biomio.algorithms.cascades.tools import loadScript
from biomio.algorithms.clustering import FOREL, KMeans
from biomio.algorithms.logger import logger


class ClustersMatchingDetector(KeypointsObjectDetector):
    def __init__(self):
        KeypointsObjectDetector.__init__(self)
        self._cascadeROI = OptimalROIDetectorSAoS()
        self._eyeROI = CascadesDetectionInterface(loadScript("main_haarcascade_eyes_union.json", True))
        self._database = []
        self._etalon = []
        self._prob = 100
        with open('keypoints.conf', 'r') as f:
            self._coff = float(f.read().replace('\n', ''))

    def threshold(self):
        return self.kodsettings.probability

    def importSettings(self, settings):
        if len(settings.keys()) > 0:
            logger.info("Settings loading started...")
            self.kodsettings.importSettings(settings['KODSettings'])
            self.kodsettings.dump()
            if self._cascadeROI is None:
                self._cascadeROI = OptimalROIDetectorSAoS()
            if self._eyeROI is None:
                self._eyeROI = CascadesDetectionInterface(loadScript("main_haarcascade_eyes_union.json", True))
            logger.info("Settings loading finished.")
            return True
        return False

    def exportSettings(self):
        return {
            'KODSettings': self.kodsettings.exportSettings()
        }

    def _detect(self, data, detector):
        # ROI detection
        rect = self._eyeROI.detect(data['roi'])[1]
        if len(rect) <= 0 or len(rect[0]) <= 0:
            logger.info("Eye ROI wasn't found.")
            self._last_error = "Eye ROI wasn't found."
            return False
        # ROI cutting
        rect = rect[0]
        lefteye = (rect[0] + rect[3], rect[1] + rect[3] / 2)
        righteye = (rect[0] + rect[2] - rect[3], rect[1] + rect[3] / 2)
        centereye = (lefteye[0] + (righteye[0] - lefteye[0]) / 2, lefteye[1] + (righteye[1] - lefteye[1]) / 2)
        centernose = (lefteye[0] + (righteye[0] - lefteye[0]) / 2, rect[1] + 2 * rect[3])
        centermouth = (centernose[0], centernose[1] + rect[3])
        leftmouth = (lefteye[0], centermouth[1])
        rightmouth = (righteye[0], centermouth[1])
        centers = [lefteye, righteye, centereye, centernose, leftmouth, rightmouth]
        # self.filter_keypoints(data)

        clusters = KMeans(data['keypoints'], 0, centers)
        data['true_clusters'] = clusters
        descriptors = []
        centers = []
        weights = []
        keydescriptors = []
        active_clusters = 0
        for cluster in clusters:
            desc = detector.compute(data['roi'], cluster['items'])
            curr_cluster = desc['descriptors']
            descriptors.append(curr_cluster)
            centers.append(cluster['center'])
            if curr_cluster is not None and len(curr_cluster) > 0:
                active_clusters += 1
            pairs = []
            sum = 0
            for index, item in enumerate(cluster['items']):
                # pairs.append((desc['descriptors'][index], item.response))
                sum += item.response
            weights.append((pairs, sum))
            cluster_keypoints = []
            for index, item in enumerate(cluster['items']):
                cluster_keypoints.append((item, desc['descriptors'][index]))
            keydescriptors.append(cluster_keypoints)
        data['clusters'] = descriptors
        data['centers'] = centers
        data['weights'] = weights
        data['key_desc'] = keydescriptors
        if active_clusters < len(centers) - 2:
            logger.info("Number of clusters are insufficient for the recognition.")
            self._last_error = "Number of clusters are insufficient for the recognition."
            return False
        return True

    def filter_keypoints(self, data):
        clusters = FOREL(data['keypoints'], 20)
        keypoints = []
        for cluster in clusters:
            p = len(cluster['items']) / (1.0 * len(data['keypoints']))
            if p > 0.02:
                keypoints += [item for item in cluster['items']]
        data['keypoints'] = keypoints
