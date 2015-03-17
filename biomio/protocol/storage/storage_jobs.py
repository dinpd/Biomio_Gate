from __future__ import absolute_import
import logging

from biomio.constants import APPS_TABLE_CLASS_NAME, USERS_TABLE_CLASS_NAME, EMAILS_TABLE_CLASS_NAME, \
    REDIS_CHANGES_CLASS_NAME, SESSION_TABLE_CLASS_NAME
from biomio.mysql_storage.mysql_data_store_interface import MySQLDataStoreInterface
from biomio.protocol.storage.application_data_store import ApplicationDataStore
from biomio.protocol.storage.redisstore import RedisStore
from biomio.protocol.storage.session_data_store import SessionDataStore
from biomio.protocol.storage.user_data_store import UserDataStore


logger = logging.getLogger(__name__)


# APP Jobs #
def create_app_job(app_id, app_public_key, user_id):
    logger.info('Creating APP, app ID - %s, user_id - %s' % (app_id, user_id))
    MySQLDataStoreInterface.create_data(APPS_TABLE_CLASS_NAME, app_id=app_id,
                                        app_public_key=app_public_key, users=user_id)
    logger.info('Created APP, app ID - %s, user_id - %s' % (app_id, user_id))


def delete_app_job(app_id):
    logger.info('Deleting APP, app_id - %s' % app_id)
    MySQLDataStoreInterface.delete_data(APPS_TABLE_CLASS_NAME, app_id)
    logger.info('Deleted APP, app_id - %s' % app_id)


def get_app_job(app_id, callback_code):
    logger.info('Getting APP, app_id - %s' % app_id)
    app = MySQLDataStoreInterface.get_object(APPS_TABLE_CLASS_NAME, object_id=app_id)
    ApplicationDataStore.instance().store_app_data(store_mysql=False, **app.to_dict())
    store_job_result(app.get_redis_key(app_id=app_id), callback_code)
    logger.debug(app.to_dict())
    logger.info('Got APP, app_id - %s' % app_id)


def select_apps_job():
    logger.info('Selecting all apps')
    result = MySQLDataStoreInterface.select_data(APPS_TABLE_CLASS_NAME)
    logger.info('Selected all apps')
    logger.debug(result)


def update_app_job(app_id, **kwargs):
    logger.info('Updating app, app_id - %s' % app_id)
    MySQLDataStoreInterface.update_data(APPS_TABLE_CLASS_NAME, object_id=app_id, **kwargs)
    logger.info('Updated app, app_id - %s' % app_id)


# User Jobs #
def create_user_job(user_id, name):
    logger.info('Creating USER, user_id - %s, name - %s' % (user_id, name))
    MySQLDataStoreInterface.create_data(USERS_TABLE_CLASS_NAME, user_id=user_id, name=name)
    logger.info('Created USER, user_id - %s, name - %s' % (user_id, name))


def get_user_job(user_id, callback_code):
    logger.info('Getting User, user_id - %s' % user_id)
    user = MySQLDataStoreInterface.get_object(USERS_TABLE_CLASS_NAME, object_id=user_id)
    UserDataStore.instance().store_user_data(store_mysql=False, **user.to_dict())
    store_job_result(user.get_redis_key(user_id=user_id), callback_code)
    logger.debug(user.to_dict())
    logger.info('Got user, user_id - %s' % user_id)


def delete_user_job(user_id):
    logger.info('Deleting User, user_id - %s' % user_id)
    MySQLDataStoreInterface.delete_data(USERS_TABLE_CLASS_NAME, object_id=user_id)
    logger.info('Deleted User, user_id - %s' % user_id)


def select_users_job():
    logger.info('Selecting all users')
    result = MySQLDataStoreInterface.select_data(USERS_TABLE_CLASS_NAME)
    logger.debug(result)
    logger.info('Selected all users')


def update_user_job(user_id, **kwargs):
    logger.info('Updating user, user_id - %s' % user_id)
    MySQLDataStoreInterface.update_data(USERS_TABLE_CLASS_NAME, object_id=user_id, **kwargs)
    logger.info('Updated user, user_id - %s' % user_id)


# Email Jobs #
def create_user_email(email, pass_phrase, public_pgp_key, user_id, private_pgp_key=None):
    logger.info('Creating and Adding user email, user_id - %s, email- %s, pass_phrase - %s, public_key - %s, '
                'private_key - %s' % (user_id, email, pass_phrase, public_pgp_key, private_pgp_key))
    MySQLDataStoreInterface.create_data(EMAILS_TABLE_CLASS_NAME, email=email, pass_phrase=pass_phrase,
                                        public_pgp_key=public_pgp_key, private_pgp_key=private_pgp_key, user=user_id)
    logger.info('Created and Added user email, user_id - %s, email- %s, pass_phrase - %s, public_key - %s, '
                'private_key - %s' % (user_id, email, pass_phrase, public_pgp_key, private_pgp_key))


def get_user_email(email):
    logger.info('Getting User email - %s' % email)
    email_object = MySQLDataStoreInterface.get_object(EMAILS_TABLE_CLASS_NAME, object_id=email)
    logger.debug(email_object.to_dict())
    logger.info('Gor User email - %s' % email)


def delete_user_email(email):
    logger.info('Deleting User email, email - %s' % email)
    MySQLDataStoreInterface.delete_data(EMAILS_TABLE_CLASS_NAME, object_id=email)
    logger.info('Deleted User email - %s' % email)


def select_user_emails():
    logger.info('Getting all User emails')
    result = MySQLDataStoreInterface.select_data(EMAILS_TABLE_CLASS_NAME)
    logger.debug(result)
    logger.info('Got all User emails')


def update_email_job(email, **kwargs):
    logger.info('Updating User email - %s' % email)
    MySQLDataStoreInterface.update_data(EMAILS_TABLE_CLASS_NAME, object_id=email, **kwargs)
    logger.info('Updated User email - %s' % email)


# Redis update job
def update_redis_job():
    logger.info('Doing REDIS UPDATE job')
    result = MySQLDataStoreInterface.select_data(REDIS_CHANGES_CLASS_NAME)
    logger.debug(result)
    for redis_keys in result:
        logger.debug('Redis Key', redis_keys.get('redis_key'))
        RedisStore.instance().delete_custom_data(redis_keys.get('redis_key'))
    logger.info('REDIS UPDATE done.')


# Session Jobs
def create_session_job(refresh_token, state, ttl):
    logger.info('Creating Session, refresh_token - %s' % refresh_token)
    MySQLDataStoreInterface.create_data(SESSION_TABLE_CLASS_NAME, refresh_token=refresh_token, state=state, ttl=ttl)
    logger.info('Created Session, refresh_token - %s' % refresh_token)


def get_session_job(refresh_token, callback_code):
    logger.info('Getting Session, refresh_token - %s' % refresh_token)
    session = MySQLDataStoreInterface.get_object(SESSION_TABLE_CLASS_NAME, object_id=refresh_token)
    redis_key = session.get_redis_key(refresh_token=refresh_token)
    SessionDataStore.instance().store_session_data(store_mysql=False, **session.to_dict())
    store_job_result(redis_key, callback_code)
    logger.debug(session.to_dict())
    logger.info('Got Session, refresh_token - %s' % refresh_token)


def update_session_job(refresh_token, **kwargs):
    logger.info('Updating session, refresh_token - %s' % refresh_token)
    MySQLDataStoreInterface.update_data(SESSION_TABLE_CLASS_NAME, object_id=refresh_token, **kwargs)
    logger.info('Updated session, refresh_token - %s' % refresh_token)


def delete_session_job(refresh_token):
    logger.info('Deleting session, refresh_token - %s' % refresh_token)
    MySQLDataStoreInterface.delete_data(SESSION_TABLE_CLASS_NAME, object_id=refresh_token)
    logger.info('Deleted session, refresh_token - %s' % refresh_token)


def store_job_result(redis_key, callback_code):
    RedisStore.instance().store_job_result('mysql_store:%s' % callback_code, **{'redis_key': redis_key})