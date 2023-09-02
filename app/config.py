import os


class BaseConfig(object):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://user:user1234@mysql:3307/db_1'


class ProductionConfig(BaseConfig):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://user:user1234@localhost:3308/db_test'
