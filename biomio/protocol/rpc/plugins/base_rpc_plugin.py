import abc
from yapsy.IPlugin import IPlugin
from biomio.worker.worker_interface import WorkerInterface


class BaseRpcPlugin(IPlugin):

    def __init__(self):
        self._worker = WorkerInterface.instance()
        super(BaseRpcPlugin, self).__init__()

    @abc.abstractmethod
    def identify_user(self, on_behalf_of):
        """
            Method that will identify user by received rpc on_behalf_of parameter.
        :param on_behalf_of: Value received in RPC request
        :return: User ID or None if user does not exists.
        """
        return

    @abc.abstractmethod
    def assign_user_to_application(self, app_id, user_id):
        """
            Assigns user to application that requested the RPC call
        :param app_id: APP ID of the current application
        :param user_id: User identifier retrieved using on_behalf_of parameter.
        """
        pass

    def _process_job(self, job_to_run, **kwargs):
        self._worker.run_job(job_to_run, **kwargs)
