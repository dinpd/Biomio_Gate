import os
from tornado.options import define, options, parse_config_file

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = os.path.join(APP_ROOT, '..', '..')

DEFAULT_CONNECTION_TTL = 30  # 30 minutes
DEFAULT_PORT = 8080
DEFAULT_DEV_MODE = False
DEFAULT_SESSION_TTL = 3 * 60  # 3 minutes
DEFAULT_REDIS_PORT = 6379
DEFAULT_REDIS_LRU_PORT = 6381
DEFAULT_REDIS_HOST = 'localhost'
DEFAULT_BIOAUTH_TIMEOUT = 5 * 60


DEFAULT_MYSQL_HOST = 'localhost'
DEFAULT_MYSQL_USER = 'biomio_user'
DEFAULT_MYSQL_PASSWORD = 'b10m10p@$$'
DEFAULT_MYSQL_DATABASE_NAME = 'biom_website'

DEFAULT_REDIS_MAX_MEMORY = '100000000'
DEFAULT_REDIS_MEMORY_SAMPLES = '5'
DEFAULT_REDIS_EVICTION_POLICY = 'allkeys-lru'


APNS_PRODUCTION_PEM = os.path.join(APP_ROOT, 'push_prod.pem')
APNS_DEV_PEM = os.path.join(APP_ROOT, 'push_dev.pem')

DEFAULT_AI_REST_URL = 'http://biom.io/backups/beta2/php/commands.php/%s'

DEFAULT_REST_PORT = 8888
DEFAULT_REST_SSL_POST = 443

DEFAULT_POLICY_TRY_TYPE = 'face-photo'

# Setting Tornado options
define('connection_timeout', default=DEFAULT_CONNECTION_TTL,
       help='Number of seconds in which inactive connection will be closed.')
define('port', default=DEFAULT_PORT)
define('dev_mode', default=DEFAULT_DEV_MODE)
define('host', default='127.0.0.1')
define('session_ttl', default=DEFAULT_SESSION_TTL, help='Number of seconds in which session expires.')
define('redis_port', default=DEFAULT_REDIS_PORT, help='Redis port')
define('redis_lru_port', default=DEFAULT_REDIS_LRU_PORT, help='Redis LRU port')
define('redis_host', default=DEFAULT_REDIS_HOST, help='Redis host address')
define('bioauth_timeout', default=DEFAULT_BIOAUTH_TIMEOUT, help='Biometric authentication timeout')

# Setting MySQL options
define('mysql_host', default=DEFAULT_MYSQL_HOST, help='MySQL server host.')
define('mysql_user', default=DEFAULT_MYSQL_USER, help='MySQL user.')
define('mysql_pass', default=DEFAULT_MYSQL_PASSWORD, help='MySQL user password.')
define('mysql_db_name', default=DEFAULT_MYSQL_DATABASE_NAME, help='MySQL database name.')

# REST settings
define('rest_port', default=DEFAULT_REST_PORT, help='REST port')
define('rest_ssl_port', default=DEFAULT_REST_SSL_POST, help='REST SSL port')

# Setting Redis options
define('redis_max_memory', default=DEFAULT_REDIS_MAX_MEMORY, help='Redis max memory option.')
define('redis_max_memory_samples', default=DEFAULT_REDIS_MEMORY_SAMPLES, help='Redis number of samples to check '
                                                                              'for every eviction.')
define('redis_eviction_policy', default=DEFAULT_REDIS_EVICTION_POLICY, help='Data eviction policy.')

define('policy_try_type', default=DEFAULT_POLICY_TRY_TYPE, help='Probe policy try type.')


# Setting REST client options
define('ai_rest_url', default=DEFAULT_AI_REST_URL, help='REST url to communicate with AI')

# options.logging = None
parse_config_file(path=os.path.join(APP_ROOT, 'biomio.conf'))
settings = options

