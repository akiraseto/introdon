import os

# Worker Processes
workers = 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

max_requests = 1000
max_requests_jitter = 50

# Sever Socket
host = '0.0.0.0'
port = os.getenv('PORT', 5000)

bind = str(host) + ':' + str(port)

# Debugging
reload = True

# Logging
capture_output = True
loglevel = 'info'
# loglevel = 'debug'
# accesslog = '-'
errorlog = '-'
# accesslog = '/var/log/gunicorn_access.log'
# errorlog = '/var/log/gunicorn_error.log'

# Proc Name
proc_name = 'gunicorn_flask'
