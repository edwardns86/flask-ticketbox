import os

from dotenv import load_dotenv
load_dotenv()

class Config(object):
    SQLALCHEMY_DATABASE_URI= os.environ.get('DATABASE_URL')
    SECRET_KEY= 'secretkey'
    MAILGUN_API= os.environ.get('MAILGUN_API')