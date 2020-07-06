import os

from dotenv import load_dotenv

SECRET_KEY = os.urandom(24)

load_dotenv('db/envfile')
MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']

# PRODUCTION環境
DEBUG = False
HOST = 'mariadb'
DB_NAME = 'introdon'

# DEV環境
if os.environ['FLASK_ENV'] == 'DEV':
    DEBUG = True
    SQLALCHEMY_RECORD_QUERIES = True

# TEST環境
if os.environ['FLASK_ENV'] == 'TEST':
    HOST = 'mariadb_test'
    DB_NAME = 'introdon_test'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}'.format(**{
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'host': HOST,
    'port': '3306',
    'db_name': DB_NAME
})

SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True
}
