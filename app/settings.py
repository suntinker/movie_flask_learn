# coding:utf8

class BaseConfig(object):
    NNN = 123
    SESSION_COOKIE_NAME = "session_sss"


class TestConfig(BaseConfig):
    DB_URI = "127.0.0.1"


class DevConfig(BaseConfig):
    DB_URI = "***"
    DB_USER = "***"
    DB_PWD = "***"


class ProConfig(BaseConfig):
    DB_URI = "127.0.0.1"
