from ..settings import *

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'btcvillage',
        'USER': 'wjdgh8926',
        'PASSWORD' : 'qlxmzhdls123',
        'HOST' : 'btcvillage.csw6nbjf0ecg.ap-northeast-2.rds.amazonaws.com',
        'PORT' : '3306',
    }
}

ALLOWED_HOSTS = ['*']


DEBUG = False