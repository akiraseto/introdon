import os

from dotenv import load_dotenv

SECRET_KEY = os.urandom(24)

# PRODUCTION環境
DEBUG = False
# DEV環境
# DEBUG = True

load_dotenv('db/envfile')
MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}'.format(**{
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'host': 'mariadb',
    'port': '3306',
    'db_name': 'introdon'
})

SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True
}
