# SQLALCHEMY_DATABASE_URI = 'sqlite:///flask_blog.db'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}'.format(**{
    'user': 'root',
    'password': 'rootroot',
    'host': 'localhost',
    'db_name': 'introdon'
})

SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG = True
SECRET_KEY = 'secret_key'
USERNAME = 'hoge'
PASSWORD = 'hoge'
