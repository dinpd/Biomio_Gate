
from tornado.options import define, options, parse_config_file

DEFAULT_CONNECTION_TTL = 30  # 30 minutes
DEFAULT_PORT = 8080
DEFAULT_SESSION_TTL = 3*60  # 3 minutes

# Setting Tornado options
define('connection_timeout', default=DEFAULT_CONNECTION_TTL, help='Number of seconds in which inactive connection will be closed.')
define('port', default=DEFAULT_PORT)
define('session_ttl', default=DEFAULT_SESSION_TTL, help='Number of seconds in which session expires.')

parse_config_file(path='biomio.conf')
settings = options

