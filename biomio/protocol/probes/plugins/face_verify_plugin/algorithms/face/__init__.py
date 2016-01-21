from clusters_db_keypoints import ClustersDBMatchingDetector
from clusters_templateL0_keypoints import ClustersTemplateL0MatchingDetector
from clusters_templateL1_keypoints import ClustersTemplateL1MatchingDetector

def getClustersMatchingDetectorWithoutTemplate():
    detector = ClustersDBMatchingDetector()
    return detector


def getClustersMatchingDetectorWithL0Template():
    detector = ClustersTemplateL0MatchingDetector()
    return detector


def getClustersMatchingDetectorWithL1Template():
    detector = ClustersTemplateL1MatchingDetector()
    return detector
