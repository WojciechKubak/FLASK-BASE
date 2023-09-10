import os


class BaseConfig(object):
    """
    Base configuration class with common settings for all environments.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://user:user1234@mysql:3307/db_1'


class ProductionConfig(BaseConfig):
    """
    Production environment configuration.
    """
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')


class DevelopmentConfig(BaseConfig):
    """
    Development environment configuration.
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):
    """
    Testing environment configuration.
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://user:user1234@localhost:3308/db_test'
