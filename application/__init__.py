from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

def get_config():
    config = {}
    if 'RDS_HOSTNAME' in os.environ:
        env = {
	    'NAME': os.environ['RDS_DB_NAME'],
	    'USER': os.environ['RDS_USERNAME'],
	    'PASSWORD': os.environ['RDS_PASSWORD'],
	    'HOST': os.environ['RDS_HOSTNAME'],
	    'PORT': os.environ['RDS_PORT'],
        }
        config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + env['USER'] + ':' + env['PASSWORD'] + '@' + env['HOST'] + ':' + env['PORT'] + '/' + env['NAME']
        config['SQLALCHEMY_POOL_RECYCLE'] = 3600
        config['WTF_CSRF_ENABLED'] = True
    else:
        config = None
    return config 

config = get_config()
application = Flask(__name__)
db = None
if config is not None:
    application.config.from_object(config)
    try:
        db = SQLAlchemy(application)
    except Exception as err:
        print(err.message)
