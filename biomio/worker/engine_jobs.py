import requests
from requests.exceptions import HTTPError
from biomio.constants import EMAILS_TABLE_CLASS_NAME, REDIS_DO_NOT_STORE_RESULT_KEY, REST_VERIFY_COMMAND, \
    USERS_TABLE_CLASS_NAME
from biomio.mysql_storage.mysql_data_store_interface import MySQLDataStoreInterface
from biomio.protocol.crypt import Crypto
from biomio.protocol.data_stores.base_data_store import BaseDataStore
from biomio.protocol.settings import settings
from logger import worker_logger


def verify_registration_job(code, app_type, callback_code):
    result = dict(verified=False)
    user_id = None
    try:
        app_verification_url = settings.ai_rest_url % (REST_VERIFY_COMMAND % (str(code), '0'))
        response = requests.post(app_verification_url)
        try:
            response.raise_for_status()
            try:
                response = response.json()
            except ValueError as e:
                worker_logger.exception(e)
                worker_logger.debug(response)
                raise Exception(e)
            user_id = response.get('user_id')
            worker_logger.debug('Received user ID - %s' % user_id)
            if user_id is None:
                result.update({'error': "Didn't receive any user ID from AI."})
            else:
                result.update({'verified': True})
        except HTTPError as e:
            worker_logger.exception(e)
            result.update({'error': response.reason})
        if result.get('verified'):
            key, pub_key = Crypto.generate_keypair()
            fingerprint = Crypto.get_public_rsa_fingerprint(pub_key)

            if app_type == 'probe':
                app_verification_url = settings.ai_rest_url % (REST_VERIFY_COMMAND % (str(code), fingerprint))
                response = requests.post(app_verification_url)
                worker_logger.debug(response.text)

            from biomio.protocol.data_stores.application_data_store import ApplicationDataStore

            ApplicationDataStore.instance().store_data(
                app_id=str(fingerprint),
                public_key=pub_key,
                app_type=app_type,
                users=int(user_id)
            )
            result.update({'app_id': fingerprint, 'private_key': key})

    except Exception as e:
        worker_logger.exception(e)
        result.update({'error': 'Sorry but we were not able to register the app: Internal error occurred.'})

    finally:
        BaseDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                  record_dict=result, callback_code=callback_code)
        worker_logger.info('Finished app registration with result: %s' % str(result))


def get_probe_ids_by_user_email(table_class_name, email, callback_code):
    worker_logger.info('Getting probe ids by user email - %s' % email)
    result = dict()
    try:
        email_data = MySQLDataStoreInterface.get_object(table_name=EMAILS_TABLE_CLASS_NAME, object_id=email)
        if email_data is not None:
            worker_logger.debug('Email Data - %s' % email_data.to_dict())
            worker_logger.debug(email_data.user)
            probe_ids = MySQLDataStoreInterface.get_applications_by_user_id_and_type(table_name=table_class_name,
                                                                                     user_id=email_data.user,
                                                                                     app_type='probe')
            worker_logger.debug('probe IDS - %s' % probe_ids)
            result.update({'result': probe_ids})
        else:
            result.update({'result': [], 'error': 'Email is not registered'})
    except Exception as e:
        worker_logger.exception(e)
        result.update({'result': [], 'error': str(e)})
    finally:
        BaseDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                  record_dict=result, callback_code=callback_code)
        worker_logger.info('Got probe ids by user email - %s' % email)


def get_extension_ids_by_probe_id(table_class_name, probe_id, callback_code):
    worker_logger.info('Getting extension ids by probe ID - %s' % probe_id)
    result = dict()
    try:
        probe_data = MySQLDataStoreInterface.get_object(table_name=table_class_name, object_id=probe_id,
                                                        return_dict=True)
        extension_ids = []
        if probe_data is not None:
            worker_logger.debug('Probe data - %s' % probe_data)
            user = MySQLDataStoreInterface.get_object(table_name=USERS_TABLE_CLASS_NAME,
                                                      object_id=probe_data.get('users')[0])
            worker_logger.debug('USer data - %s' % user.to_dict())
            extension_ids = MySQLDataStoreInterface.get_applications_by_user_id_and_type(table_name=table_class_name,
                                                                                         user_id=user,
                                                                                         app_type='extension')
            worker_logger.debug('Extension IDS - %s' % extension_ids)
        else:
            worker_logger.info('No record for probe id - %s' % probe_id)
        result.update({'result': extension_ids})
    except Exception as e:
        worker_logger.exception(e)
        result.update({'error': str(e)})
    finally:
        BaseDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                  record_dict=result, callback_code=callback_code)
        worker_logger.info('Got extension ids by probe ID - %s' % probe_id)
