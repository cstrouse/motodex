import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')

    POSTGRES_USER = os.getenv('POSTGRES_USER', 'motodex')
    POSTGRES_PW = os.getenv('POSTGRES_PW', 'motodex')
    POSTGRES_URL = os.getenv('POSTGRES_URL', '127.0.0.1:5432')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'motodex')

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW,
                                                                                    url=POSTGRES_URL, db=POSTGRES_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False
    WTF_CSRF_ENABLED = False


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    ASSETS_DEBUG = True

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = os.getenv('MAIL_PORT', 587)
    MAIL_USE_TLS = bool(os.getenv('MAIL_USE_TLS', True))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'bwblock3@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'test')


class TestConfig(Config):
    ENV = 'test'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_ECHO = True
