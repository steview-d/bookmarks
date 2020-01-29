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

    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
               'AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/70.0.3538.77 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,'
               'application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}
