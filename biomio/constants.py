# Pony Entities constants.

TABLES_MODULE = 'mysql_data_entities'

APPS_TABLE_CLASS_NAME = 'AppInformation'
USERS_TABLE_CLASS_NAME = 'UserInformation'
EMAILS_TABLE_CLASS_NAME = 'EmailPGPInformation'
REDIS_CHANGES_CLASS_NAME = 'ChangesTable'
SESSION_TABLE_CLASS_NAME = 'SessionData'

# Redis Constants

REDIS_APPLICATION_KEY = 'application:%s'
REDIS_USER_KEY = 'user:%s'
REDIS_EMAILS_KEY = 'email:%s'
REDIS_SESSION_KEY = 'token:%s'
REDIS_JOB_RESULT_KEY = 'job_result:%s:%s'

# Other constants
REDIS_CONFIG_MAX_MEMORY_OPTION_KEY = 'maxmemory'
REDIS_CONFIG_MEMORY_SAMPLES_OPTION_KEY = 'maxmemory-samples'
REDIS_CONFIG_EVICTION_POLICY_OPTION_KEY = 'maxmemory-policy'