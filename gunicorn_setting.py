import os

# Worker Processes
workers = 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Sever Socket
host = '0.0.0.0'
port = os.getenv('PORT', 5000)

bind = str(host) + ':' + str(port)

# Debugging
reload = True

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'debug'
# nginxのlogで十分と判断
# accesslog = '/var/log/gunicorn_access.log'
# errorlog = '/var/log/gunicorn_error.log'
# loglevel = 'info'

# Proc Name
proc_name = 'gunicorn_flask'
