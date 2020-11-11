from decouple import config

class Config:
    pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:787898@127.0.0.1/apiflask'
	SQLALCHEMY_TRACK_MODIFICATIONS= False

class TestConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:787898@127.0.0.1/apiflask_test'
	SQLALCHEMY_TRACK_MODIFICATIONS= False

config = {
    'test': TestConfig,
    'development': DevelopmentConfig
}