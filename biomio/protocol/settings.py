from tornado.options import define, options, parse_config_file

DEFAULT_CONNECTION_TTL = 30  # 30 minutes
DEFAULT_PORT = 8080
DEFAULT_SESSION_TTL = 3*60  # 3 minutes
DEFAULT_REDIS_PORT = 6379
DEFAULT_REDIS_HOST = 'localhost'

# Setting Tornado options
define('connection_timeout', default=DEFAULT_CONNECTION_TTL, help='Number of seconds in which inactive connection will be closed.')
define('port', default=DEFAULT_PORT)
define('host', default='127.0.0.1')
define('session_ttl', default=DEFAULT_SESSION_TTL, help='Number of seconds in which session expires.')
define('redis_port', default=DEFAULT_REDIS_PORT, help='Redis port')
define('redis_host', default=DEFAULT_REDIS_HOST, help='Redis host address')

parse_config_file(path='../../biomio.conf')
settings = options

