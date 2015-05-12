# Pony Entities constants.

TABLES_MODULE = 'mysql_data_entities'

APPS_TABLE_CLASS_NAME = 'Application'
USERS_TABLE_CLASS_NAME = 'UserInformation'
EMAILS_TABLE_CLASS_NAME = 'EmailsData'
REDIS_CHANGES_CLASS_NAME = 'ChangesTable'
TRAINING_DATA_TABLE_CLASS_NAME = 'TrainingData'

MYSQL_APPS_TABLE_NAME = 'Applications'
MYSQL_EMAILS_TABLE_NAME = 'EmailsData'
MYSQL_USERS_TABLE_NAME = 'Profiles'
MYSQL_TRAINING_DATA_TABLE_NAME = 'TrainingData'

# Redis Constants
REDIS_APP_AUTH_KEY = 'auth:%s'
REDIS_APP_CONNECTION_KEY = 'connection:%s'
REDIS_APPLICATION_KEY = 'application:%s'
REDIS_USER_KEY = 'user:%s'
REDIS_EMAILS_KEY = 'email:%s'
REDIS_SESSION_KEY = 'token:%s'
REDIS_JOB_RESULT_KEY = 'job_result:%s:%s'
REDIS_DO_NOT_STORE_RESULT_KEY = 'do_not_store:%s'
REDIS_PROBE_RESULT_KEY = 'probe_result:%s'
REDIS_RESULTS_COUNTER_KEY = 'job_results_counter:%s'
REDIS_PARTIAL_RESULTS_KEY = 'job_results_gatherer:%s'
REDIS_JOB_RESULTS_ERROR = 'job_results_error:%s:%s'

# Other constants
REDIS_CONFIG_MAX_MEMORY_OPTION_KEY = 'maxmemory'
REDIS_CONFIG_MEMORY_SAMPLES_OPTION_KEY = 'maxmemory-samples'
REDIS_CONFIG_EVICTION_POLICY_OPTION_KEY = 'maxmemory-policy'

MODULES_CLASSES_BY_TABLE_NAMES = {
    MYSQL_APPS_TABLE_NAME: dict(
        module_name='biomio.protocol.data_stores.application_data_store',
        class_name='ApplicationDataStore'
    ),
    MYSQL_EMAILS_TABLE_NAME: dict(
        module_name='biomio.protocol.data_stores.email_data_store',
        class_name='EmailDataStore'
    )
}