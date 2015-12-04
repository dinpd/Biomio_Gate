from biomio.algorithms.interfaces import AlgorithmInterface

class VerificationSAInterface(AlgorithmInterface):
    def __init__(self):
        pass

    def training(self, callback=None, **kwargs):
        pass

    def apply(self, callback=None, **kwargs):
        pass
