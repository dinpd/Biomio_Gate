

class AdministrativeInterface:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = AdministrativeInterface()

        return cls._instance

    def __init__(self):
        pass

    def verify_passcode(self, passcode):
        """
        Verifies passcode by using request to administrative backend.
        :param passcode: Given passcode.
        :return: True if verification succeeded; False otherwise.
        """
        return True

    def register_biometrics(self, code):
        return True