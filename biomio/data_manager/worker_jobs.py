from data_manager import DataManager

TABLES_MODULE = 'mysql_entities'


def save_data_job():
    print 'Doing SAVE job.'
    data_manager = DataManager.instance()
    data_manager.insert_data(TABLES_MODULE, 'Test1', name='Test1', value=2)
    print 'SAVE Job done.'


def get_data_job():
    print 'Doing GET job.'
    data_manager = DataManager.instance()
    result = data_manager.get_data(TABLES_MODULE, 'Test1')
    print result
    print 'GET job done.'


def update_data_job():
    print 'Doing UPDATE job'
    data_manager = DataManager.instance()
    data_manager.update_data(TABLES_MODULE, 'Test1', 1, name='Test2', value=3)
    print 'Update JOB done.'
