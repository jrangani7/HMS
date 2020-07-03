import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "Secret_string"
    MYSQL_DATABASE_HOST='localhost'
    MYSQL_DATABASE_PORT=3306
    MYSQL_DATABASE_USER='root'
    MYSQL_DATABASE_PASSWORD='root'
    MYSQL_DATABASE_DB='tcs_hms'
