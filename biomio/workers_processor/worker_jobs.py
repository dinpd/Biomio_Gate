import logging
from biomio.protocol.mysql_storage.mysql_data_store_interface import DataManagerInterface
from biomio.protocol.storage.redisstore import RedisStore

logger = logging.getLogger(__name__)

TABLES_MODULE = 'mysql_entities'

APPS_TABLE_CLASS_NAME = 'AppInformation'
USERS_TABLE_CLASS_NAME = 'UserInformation'
EMAILS_TABLE_CLASS_NAME = 'EmailPGPInformation'
REDIS_CHANGES_CLASS_NAME = 'ChangesTable'


# APP Jobs #
def create_app_job(app_id, app_public_key, user_id):
    logger.info('Creating APP, app ID - %s, user_id - %s' % (app_id, user_id))
    DataManagerInterface.create_data(TABLES_MODULE, APPS_TABLE_CLASS_NAME, app_id=app_id,
                                     app_public_key=app_public_key, users=user_id)
    logger.info('Created APP, app ID - %s, user_id - %s' % (app_id, user_id))


def delete_app_job(app_id):
    logger.info('Deleting APP, app_id - %s' % app_id)
    DataManagerInterface.delete_data(TABLES_MODULE, APPS_TABLE_CLASS_NAME, app_id)
    logger.info('Deleted APP, app_id - %s' % app_id)


def get_app_job(app_id):
    logger.info('Getting APP, app_id - %s' % app_id)
    app = DataManagerInterface.get_object(TABLES_MODULE, APPS_TABLE_CLASS_NAME, object_id=app_id)
    logger.info('Got APP, app_id - %s' % app_id)
    logger.debug(app.to_dict())


def select_apps_job():
    logger.info('Selecting all apps')
    result = DataManagerInterface.select_data(TABLES_MODULE, APPS_TABLE_CLASS_NAME)
    logger.info('Selected all apps')
    logger.debug(result)


# User Jobs #
def create_user_job(user_id, name):
    logger.info('Creating USER, user_id - %s, name - %s' % (user_id, name))
    DataManagerInterface.create_data(TABLES_MODULE, USERS_TABLE_CLASS_NAME, user_id=user_id, name=name)
    logger.info('Created USER, user_id - %s, name - %s' % (user_id, name))


def get_user_job(user_id):
    logger.info('Getting User, user_id - %s' % user_id)
    user = DataManagerInterface.get_object(TABLES_MODULE, USERS_TABLE_CLASS_NAME, object_id=user_id)
    logger.debug(user.to_dict())
    logger.info('Got user, user_id - %s' % user_id)


def delete_user_job(user_id):
    logger.info('Deleting User, user_id - %s' % user_id)
    DataManagerInterface.delete_data(TABLES_MODULE, USERS_TABLE_CLASS_NAME, object_id=user_id)
    logger.info('Deleted User, user_id - %s' % user_id)


def select_users_job():
    logger.info('Selecting all users')
    result = DataManagerInterface.select_data(TABLES_MODULE, USERS_TABLE_CLASS_NAME)
    logger.debug(result)
    logger.info('Selected all users')


# Email Jobs #
def create_user_email(email, pass_phrase, public_pgp_key, user_id, private_pgp_key=None):
    logger.info('Creating and Adding user email, user_id - %s, email- %s, pass_phrase - %s, public_key - %s, '
                'private_key - %s' % (user_id, email, pass_phrase, public_pgp_key, private_pgp_key))
    DataManagerInterface.create_data(TABLES_MODULE, EMAILS_TABLE_CLASS_NAME, email=email, pass_phrase=pass_phrase,
                                     public_pgp_key=public_pgp_key, private_pgp_key=private_pgp_key, user=user_id)
    logger.info('Created and Added user email, user_id - %s, email- %s, pass_phrase - %s, public_key - %s, '
                'private_key - %s' % (user_id, email, pass_phrase, public_pgp_key, private_pgp_key))


def get_user_email(email):
    logger.info('Getting User email - %s' % email)
    email_object = DataManagerInterface.get_object(TABLES_MODULE, EMAILS_TABLE_CLASS_NAME, object_id=email)
    logger.debug(email_object.to_dict())
    logger.info('Gor User email - %s' % email)


def delete_user_email(email):
    logger.info('Deleting User email, email - %s' % email)
    DataManagerInterface.delete_data(TABLES_MODULE, EMAILS_TABLE_CLASS_NAME, object_id=email)
    logger.info('Deleted User email - %s' % email)


def select_user_emails():
    logger.info('Getting all User emails')
    result = DataManagerInterface.select_data(TABLES_MODULE, EMAILS_TABLE_CLASS_NAME)
    logger.debug(result)
    logger.info('Got all User emails')


# Redis update job #
def update_redis_job():
    logger.info('Doing REDIS UPDATE job')
    result = DataManagerInterface.select_data(TABLES_MODULE, REDIS_CHANGES_CLASS_NAME)
    logger.debug(result)
    for redis_keys in result:
        logger.debug('Redis Key', redis_keys.get('redis_key'))
        RedisStore.instance().delete_data(redis_keys.get('redis_key'))
    logger.info('REDIS UPDATE done.')
