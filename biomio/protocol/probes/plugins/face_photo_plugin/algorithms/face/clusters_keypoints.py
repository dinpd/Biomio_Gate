from __future__ import absolute_import
import logger
from biomio.algorithms.algorithms.clustering.forel import FOREL
from biomio.algorithms.algorithms.clustering.kmeans import KMeans
from biomio.algorithms.algorithms.cascades.classifiers import CascadeROIDetector
from biomio.algorithms.algorithms.recognition.keypoints import KeypointsObjectDetector


class ClustersMatchingDetector(KeypointsObjectDetector):
    def __init__(self):
        KeypointsObjectDetector.__init__(self)
        self._database = []
        self._etalon = []
        self._prob = 100
        self._coff = 0.9

    def threshold(self):
        return self.kodsettings.probability

    def importSettings(self, settings):
        if len(settings.keys()) > 0:
            logger.algo_logger.info("Settings loading started...")
            self.kodsettings.importSettings(settings['KODSettings'])
            self.kodsettings.dump()
            if self._cascadeROI is None:
                self._cascadeROI = CascadeROIDetector()
            self._cascadeROI.importSettings(settings['Face Cascade Detector'])
            logger.algo_logger.info('Face Cascade Detector')
            self._cascadeROI.classifierSettings.dump()
            if self._eyeROI is None:
                self._eyeROI = CascadeROIDetector()
            self._eyeROI.importSettings(settings['Eye Cascade Detector'])
            logger.algo_logger.info('Eye Cascade Detector')
            self._eyeROI.classifierSettings.dump()
            logger.algo_logger.info("Settings loading finished.")
            return True
        return False

    def exportSettings(self):
        return {
            'KODSettings': self.kodsettings.exportSettings(),
            'Face Cascade Detector': self._cascadeROI.exportSettings(),
            'Eye Cascade Detector': self._eyeROI.exportSettings()
        }

    def _detect(self, data, detector):
        # ROI detection
        rect = self._eyeROI.detectAndJoin(data['roi'], False)
        if len(rect) <= 0:
            logger.algo_logger.info("Eye ROI wasn't found.")
            self._last_error = "Eye ROI wasn't found."
            return False
        # ROI cutting
        lefteye = (rect[0] + rect[3], rect[1] + rect[3] / 2)
        righteye = (rect[0] + rect[2] - rect[3], rect[1] + rect[3] / 2)
        centereye = (lefteye[0] + (righteye[0] - lefteye[0]) / 2, lefteye[1] + (righteye[1] - lefteye[1]) / 2)
        centernose = (lefteye[0] + (righteye[0] - lefteye[0]) / 2, rect[1] + 2 * rect[3])
        centermouth = (centernose[0], centernose[1] + rect[3])
        leftmouth = (lefteye[0], centermouth[1])
        rightmouth = (righteye[0], centermouth[1])
        centers = [lefteye, righteye, centereye, centernose, leftmouth, rightmouth]
        self.filter_keypoints(data)

        clusters = KMeans(data['keypoints'], 0, centers)
        data['true_clusters'] = clusters
        descriptors = []
        active_clusters = 0
        for cluster in clusters:
            desc = detector.computeImage(data['roi'], cluster['items'])
            curr_cluster = desc['descriptors']
            descriptors.append(curr_cluster)
            if curr_cluster is not None and len(curr_cluster) > 0:
                active_clusters += 1
        data['clusters'] = descriptors
        if active_clusters < len(centers) - 2:
            logger.algo_logger.info("Number of clusters are insufficient for the recognition.")
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
