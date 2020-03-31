import os

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}'.format(**{
    'user': 'root',
    'password': 'rootroot',
    'host': 'localhost',
    'db_name': 'introdon'
})

SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG = True
SECRET_KEY = os.urandom(24)
