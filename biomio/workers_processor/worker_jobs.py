from biomio.data_manager.data_manager_interface import DataManagerInterface

TABLES_MODULE = 'mysql_entities'


def save_data_job():
    print 'Doing SAVE job.'
    DataManagerInterface.create_data(TABLES_MODULE, 'Test1', name='Test1', value=2)
    print 'SAVE Job done.'


def get_data_job():
    print 'Doing GET job.'
    result = DataManagerInterface.get_data(TABLES_MODULE, 'Test1')
    print result
    print 'GET job done.'


def update_data_job():
    print 'Doing UPDATE job'
    DataManagerInterface.update_data(TABLES_MODULE, 'Test1', 1, name='Test2', value=3)
    print 'Update JOB done.'
