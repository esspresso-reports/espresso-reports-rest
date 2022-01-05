import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    RESTX_ERROR_404_HELP = False
    ESPRESSO_ADMIN_ROLE = 'espresso_admin'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = os.getenv("ESPRESSO_DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ESPRESSO_IDP_INTROSPECT_URL = 'http://localhost:8080/auth/realms/EspressoReports/protocol/openid-connect/token/introspect'
    ESPRESSO_KC_CLIENT_ID = 'espresso'
    ESPRESSO_KC_CLIENT_SECRET = '3d087edb-3fa1-4df8-b6ed-579b13cfcdcf'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("ESPRESSO_DATABASE_URL")


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)
