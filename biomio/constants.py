# Pony Entities constants.

TABLES_MODULE = 'mysql_data_entities'

APPS_TABLE_CLASS_NAME = 'AppInformation'
USERS_TABLE_CLASS_NAME = 'UserInformation'
EMAILS_TABLE_CLASS_NAME = 'EmailPGPInformation'
REDIS_CHANGES_CLASS_NAME = 'ChangesTable'

# Redis Constants

REDIS_APPLICATION_KEY = 'application:%s'
REDIS_USER_KEY = 'user:%s'
REDIS_EMAILS_KEY = 'email:%s'