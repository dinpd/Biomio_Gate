from biomio.data_manager.data_manager_interface import DataManagerInterface
from biomio.protocol.redisstore import RedisStore


TABLES_MODULE = 'mysql_entities'


def create_app_job(app_id, app_public_key, user_id):
    print 'Creating APP, app ID - %s, user_id - %s' % (app_id, user_id)
    DataManagerInterface.create_data(TABLES_MODULE, 'AppInformation', app_id=app_id,
                                     app_public_key=app_public_key, users=user_id)
    # DataManagerInterface.update_data_set(TABLES_MODULE, 'AppInformation', update_object_id=app_id,
    #                                      add_table_name='UserInformation', add_object_id=user_id, set_attr='users')
    print 'Created APP, app ID - %s, user_id - %s' % (app_id, user_id)


def create_user_job(user_id, name):
    print 'Creating USER, user_id - %s, name - %s' % (user_id, name)
    DataManagerInterface.create_data(TABLES_MODULE, 'UserInformation', user_id=user_id, name=name)
    print 'Created USER, user_id - %s, name - %s' % (user_id, name)


def create_add_user_email(email, pass_phrase, public_pgp_key, user_id, private_pgp_key=None):
    print 'Creating and Adding user email, user_id - %s, email- %s, pass_phrase - %s, public_key - %s, ' \
          'private_key - %s' % (user_id, email, pass_phrase, public_pgp_key, private_pgp_key)
    DataManagerInterface.create_data(TABLES_MODULE, 'EmailPGPInformation', email=email, pass_phrase=pass_phrase,
                                     public_pgp_key=public_pgp_key, private_pgp_key=private_pgp_key, user=user_id)
    # DataManagerInterface.update_data_set(TABLES_MODULE, 'UserInformation', update_object_id=user_id,
    #                                      add_table_name='EmailPGPInformation', add_object_id=email, set_attr='emails')
    print 'Created and Added user email, user_id - %s, email- %s, pass_phrase - %s, public_key - %s, ' \
          'private_key - %s' % (user_id, email, pass_phrase, public_pgp_key, private_pgp_key)


def delete_app_job(app_id):
    print 'Deleting APP, app_id - %s' % app_id
    DataManagerInterface.delete_data(TABLES_MODULE, 'AppInformation', app_id)
    print 'Deleted APP, app_id - %s' % app_id


def update_redis_job():
    print 'Doing REDIS UPDATE job'
    result = DataManagerInterface.get_data(TABLES_MODULE, 'ChangesTable')
    for redis_keys in result.values():
        print 'Redis Key', redis_keys.get('redis_key')
        RedisStore.instance().get_redis_session().delete(redis_keys.get('redis_key'))
    print 'REDIS UPDATE done.'