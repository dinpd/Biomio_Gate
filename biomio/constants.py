# Pony Entities constants.

TABLES_MODULE = 'mysql_data_entities'

APPS_TABLE_CLASS_NAME = 'Application'
USERS_TABLE_CLASS_NAME = 'UserInformation'
EMAILS_TABLE_CLASS_NAME = 'Email'
REDIS_CHANGES_CLASS_NAME = 'ChangesTable'
TRAINING_DATA_TABLE_CLASS_NAME = 'TrainingData'
POLICY_DATA_TABLE_CLASS_NAME = 'Policy'
DEVICE_INFORMATION_TABLE_CLASS_NAME = 'DeviceInformation'
PGP_KEYS_DATA_TABLE_CLASS_NAME = 'PgpKeysData'
WEB_RESOURCE_TABLE_CLASS_NAME = 'WebResource'
PROVIDER_USERS_TABLE_CLASS_NAME = 'ProviderUser'

MYSQL_APPS_TABLE_NAME = 'Applications'
MYSQL_EMAILS_TABLE_NAME = 'Emails'
MYSQL_PGP_KEYS_TABLE_NAME = 'PgpKeysData'
MYSQL_USERS_TABLE_NAME = 'Profiles'
MYSQL_TRAINING_DATA_TABLE_NAME = 'TrainingData'
MYSQL_CHANGES_TABLE_NAME = 'UILog'
MYSQL_POLICIES_TABLE_NAME = 'Policies'
MYSQL_DEVICE_INFORMATION_TABLE_NAME = 'UserServices'
MYSQL_WEB_RESOURCES_TABLE_NAME = 'WebResources'
MYSQL_PROVIDER_USERS_TABLE_NAME = 'ProviderUsers'
# Identification Data Tables
MYSQL_IDENTIFICATION_USER_HASH_TABLE_NAME = 'IdentificationUsersBucketsData'
MYSQL_IDENTIFICATION_HASH_DATA_TABLE_NAME = 'IdentificationHashData'

# Redis Constants
REDIS_BIOMIO_GENERAL_CHANNEL = 'biomio_general:%s'
REDIS_APP_AUTH_KEY = 'auth:%s'
REDIS_APP_CONNECTION_KEY = 'connection:%s'
REDIS_APPLICATION_KEY = 'application:%s'
REDIS_USER_KEY = 'user:%s'
REDIS_EMAILS_KEY = 'email:%s'
REDIS_PGP_DATA_KEY = 'pgp_data:%s'
REDIS_SESSION_KEY = 'token:%s'
REDIS_JOB_RESULT_KEY = 'job_result:%s:%s'
REDIS_DO_NOT_STORE_RESULT_KEY = 'do_not_store:%s'
REDIS_PROBE_RESULT_KEY = 'probe_result:%s'
REDIS_RESULTS_COUNTER_KEY = 'job_results_counter:%s'
REDIS_PARTIAL_RESULTS_KEY = 'job_results_gatherer:%s'
REDIS_JOB_RESULTS_ERROR = 'job_results_error:%s'
REDIS_ACTIVE_DEVICES_KEY = 'active_devices_relations:%s'
REDIS_UPDATE_TRAINING_KEY = 'update_training:%s'
REDIS_RESOURCES_KEY = 'device_resources:%s'
REDIS_USER_POLICY_KEY = 'policy:%s'
REDIS_USER_CONDITION_KEY = 'auth_condition:%s'
REDIS_DEVICE_INFORMATION_KEY = 'device_info:%s'
REDIS_WEB_RESOURCE_KEY = 'web_resource:%s'
REDIS_PROVIDER_USER_KEY = 'provider_user:%s'

REDiS_TRAINING_RETRIES_COUNT_KEY = 'training_retries_count:%s'
REDIS_VERIFICATION_RETIES_COUNT_KEY = 'verification_retries_count:%s'

REDIS_ACTIVE_PROBE_DEVICES = 'active_probes_list'
REDIS_ACTIVE_CLIENT_CONNECTIONS = 'active_clients_list'

REDIS_IDENTIFICATION_USERS_DATA_KEY = 'identification_users_data:%s'
REDIS_IDENTIFICATION_HASH_DATA_KEY = 'identification_hash_data:%s'

# Other constants
REDIS_CONFIG_MAX_MEMORY_OPTION_KEY = 'maxmemory'
REDIS_CONFIG_MEMORY_SAMPLES_OPTION_KEY = 'maxmemory-samples'
REDIS_CONFIG_EVICTION_POLICY_OPTION_KEY = 'maxmemory-policy'

MODULES_CLASSES_BY_TABLE_NAMES = {
    MYSQL_APPS_TABLE_NAME: dict(
        module_name='biomio.protocol.data_stores.application_data_store',
        class_name='ApplicationDataStore'
    ),
    MYSQL_PGP_KEYS_TABLE_NAME: dict(
        module_name='biomio.protocol.data_stores.pgp_keys_data_store',
        class_name='PgpKeysDataStore'
    )
}

# REST Commands
REST_VERIFY_COMMAND = 'verify_service/%s/%s'
REST_CREATE_EMAIL_KEYS = 'get_user/%s'
REST_REGISTER_BIOMETRICS = 'register_biometrics/%s/%s'
REST_BIOAUTH_LOGIN = 'bioauth/%s/%s'

TRAINING_FACE_TYPE = 'face'
TRAINING_FINGER_TYPE = 'fingerprints'
TRAINING_VOICE_TYPE = 'voice'

TRAINING_GATE_AI_TYPES_MAP = {
    TRAINING_FACE_TYPE: 'face',
    TRAINING_FINGER_TYPE: 'fingerprints',
    TRAINING_VOICE_TYPE: 'voice'
}

AUTH_CANCELED_STATUS = 'canceled'
AUTH_CANCELED_MESSAGE = 'Authentication was canceled'
AUTH_FAILED_STATUS = 'failed'
AUTH_FAILED_MESSAGE = 'Authentication failed'
AUTH_MAX_RETRIES_STATUS = AUTH_FAILED_STATUS
AUTH_MAX_RETRIES_MESSAGE = 'Maximum number of auth retries reached'

TRAINING_CANCELED_STATUS = 'canceled'
TRAINING_CANCELED_MESSAGE = 'Training was canceled'
TRAINING_FAILED_STATUS = 'failed'
TRAINING_FAILED_MESSAGE = 'Training failed. Try to change your location or your device position'
TRAINING_MAX_RETRIES_STATUS = TRAINING_FAILED_STATUS
TRAINING_MAX_RETRIES_MESSAGE = 'Maximum number of training retries reached.Try to change your location or your ' \
                               'device position'
TRAINING_STARTED_STATUS = 'in-progress'
TRAINING_STARTED_MESSAGE = 'Training started'
TRAINING_RETRY_STATUS = 'retry'
TRAINING_RETRY_MESSAGE = 'Additional data is required, please check your device'
TRAINING_SUCCESS_STATUS = 'success'
TRAINING_SUCCESS_MESSAGE = 'Our recognition algorithm was successfully trained with your face data'

TRAINING_TYPES_AI_RESPONSE = {
    'face': '0',
    'fingerprints': ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    'voice': '0'
}


HYBRID_APP_TYPE_PREFIX = 'hybrid'
PROBE_APP_TYPE_PREFIX = 'probe'
GENERAL_SUBSCRIBE_PATTERN = '__keyspace*:{redis_key_pattern}'


def get_ai_training_response(training_type):
    response = TRAINING_TYPES_AI_RESPONSE
    response.update({TRAINING_GATE_AI_TYPES_MAP.get(training_type, ''): '1'})
    return response
