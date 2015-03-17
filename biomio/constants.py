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

# Other constants

USER_DATA_PREFIX = 'user_data_%s'
APP_DATA_PREFIX = 'app_data_%s'
EMAIL_DATA_PREFIX = 'email_data_%s'
SESSION_DATA_PREFIX = 'session_data_%s'