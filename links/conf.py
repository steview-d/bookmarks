from django.conf import settings
from appconf import AppConf


class MyAppConf(AppConf):

    APP_VERSION = '0.3'

    # app settings for standard users
    STND_MAX_BOOKMARKS = 500
    STND_MAX_COLLECTIONS = 20
    STND_MAX_PAGES = 2

    # app settings for premium users
    PREM_MAX_BOOKMARKS = 10000
    PREM_MAX_COLLECTIONS = 500
    PREM_MAX_PAGES = 50
