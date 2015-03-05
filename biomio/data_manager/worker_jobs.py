from data_manager import DataManager


def save_data_job():
    print 'Doing SAVE job.'
    data_manager = DataManager.instance()
    data_manager.insert_data()
    print 'SAVE Job done.'


def get_data_job():
    print 'Doing GET job.'
    data_manager = DataManager.instance()
    data_manager.get_data('mysql_entities', 'Test1')
    print 'GET job done.'