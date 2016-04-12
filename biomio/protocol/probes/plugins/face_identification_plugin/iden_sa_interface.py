import os

from biomio.algorithms.recognition.processes import (TrainingProcess, DataDetectionProcess, ClusterMatchingProcess,
                                                     RotationDetectionProcess, RotationResultProcess,
                                                     UpdateDataStructureProcess, IdentificationProcess,
                                                     IdentificationREProcess)
from biomio.algorithms.datastructs.nearpyhash import NearPyHash, NearPyHashSettings
from biomio.algorithms.recognition.processes.defs import STATUS_RESULT, STATUS_ERROR
from biomio.algorithms.recognition.processes.handling import load_temp_data
from biomio.algorithms.interfaces import AlgorithmInterface, logger
from defs import TRAINING_FULL, TEMP_DATA_PATH

class IdentificationSAInterface(AlgorithmInterface):
    def __init__(self):
        self.engines = [None, None, None, None, None, None]
        self.db_settings = NearPyHashSettings()
        self.db_settings.dimension = 64

    def training(self, **kwargs):
        mode = kwargs.get("mode", TRAINING_FULL)
        databases = {}
        if mode == TRAINING_FULL:
            train_process = TrainingProcess(TEMP_DATA_PATH)
            data_detect_process = DataDetectionProcess(TEMP_DATA_PATH)
            rotation_detect_process = RotationDetectionProcess(TEMP_DATA_PATH)
            rotation_result_process = RotationResultProcess(TEMP_DATA_PATH)
            cluster_matching_process = ClusterMatchingProcess()
            if not os.path.exists(TEMP_DATA_PATH):
                os.mkdir(TEMP_DATA_PATH, 0o777)
                os.chmod(TEMP_DATA_PATH, 0o777)
            template = {}
            for image_path in kwargs["data"]:
                settings = kwargs.copy()
                del settings["data"]
                settings['path'] = image_path
                result = train_process.process(**settings)
                if result['status'] == STATUS_ERROR:
                    logger.logger.debug("Error")
                elif result['status'] == STATUS_RESULT:
                    res = result.get('data', [])
                    if result['type'] == 'detection' and len(res) == 1:
                        result = res[0]
                    elif result['type'] == 'rotation' and len(res) == 2:
                        result = []
                        for r in res[0]:
                            settings = res[1].copy()
                            settings.update(r)
                            result.append({'data_file': rotation_detect_process.process(**settings)})
                        result = rotation_result_process.process(**{'data_list': result}).get("data", {})
                    else:
                        logger.info(ERROR_FORMAT % (INTERNAL_TRAINING_ERROR, "Invalid Data Format."))
                    result = data_detect_process.process(**result)
                    if result.get("status", "") == "error":
                        continue
                    result = load_temp_data(result['data'][0]['data_file'], remove=False)
                    if len(template) <= 0:
                        template = result["clusters"]
                    else:
                        for inx, cluster in result["clusters"].iteritems():
                            if len(template[inx]) > 0:
                                template[inx] = cluster
                            else:
                                job_data = {
                                    'cluster': cluster,
                                    'template': template[inx],
                                    'userID': result['userID'],
                                    'algoID': result['algoID'],
                                    'cluster_id': inx
                                }
                                template[inx] = cluster_matching_process.process(**job_data)
            databases[kwargs["userID"]] = template
        else:
            databases = kwargs.get("databases", {})
        update_process = UpdateDataStructureProcess()
        print databases.keys()
        for key, database in databases.iteritems():
            for inx, cluster in database.iteritems():
                ddict = {
                    "database": self.engines[int(inx)],
                    "template": cluster,
                    "uuid": key,
                    "settings": {
                        "database_type": NearPyHash.type(),
                        "settings":  self.db_settings
                    }
                }
                self.engines[int(inx)] = update_process.process(**ddict)
        print self.engines

    def apply(self, **kwargs):
        identification_process = IdentificationProcess()
        data = kwargs["data"]
        res = []
        test_size = 0
        print self.engines
        print data
        for inx, cluster in enumerate(data):
            test_size += len(cluster)
            ddict = {
                "cluster": cluster,
                "database": self.engines[inx],
                "cluster_id": inx
            }
            res.append(identification_process.process(**ddict))
        estimate_process = IdentificationREProcess()
        rests = {
            "results": res,
            "test_size": test_size
        }
        estimate_process.process(**rests)
