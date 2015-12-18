import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
TEMP_DATA_PATH = os.path.join(APP_ROOT, "temp_results")

TRAINING_FULL = "training::full"
TRAINING_HASH = "training::hash"

import cPickle
import base64

def serialize(data):
    return base64.b64encode(cPickle.dumps(data, cPickle.HIGHEST_PROTOCOL))

def deserialize(data):
    return cPickle.loads(base64.b64decode(data))
