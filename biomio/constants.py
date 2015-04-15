# Pony Entities constants.

TABLES_MODULE = 'mysql_data_entities'

APPS_TABLE_CLASS_NAME = 'Application'
USERS_TABLE_CLASS_NAME = 'UserInformation'
EMAILS_TABLE_CLASS_NAME = 'EmailsData'
REDIS_CHANGES_CLASS_NAME = 'ChangesTable'

MYSQL_APPS_TABLE_NAME = 'Applications'
MYSQL_EMAILS_TABLE_NAME = 'EmailsData'
MYSQL_USERS_TABLE_NAME = 'Profiles'

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

# Other constants
REDIS_CONFIG_MAX_MEMORY_OPTION_KEY = 'maxmemory'
REDIS_CONFIG_MEMORY_SAMPLES_OPTION_KEY = 'maxmemory-samples'
REDIS_CONFIG_EVICTION_POLICY_OPTION_KEY = 'maxmemory-policy'