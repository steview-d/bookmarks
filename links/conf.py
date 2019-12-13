from django.conf import settings
from appconf import AppConf


class MyAppConf(AppConf):
    APP_VERSION = '0.3'
