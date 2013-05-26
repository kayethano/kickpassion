from kickpassion.settings import *
import dj_database_url
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASES = {'default':
                   dj_database_url.config(
                  default='postgres://mario:5xaf9j9u@localhost:5432/kickpassion')
        }

#CuantoDev Facebook Settings
FACEBOOK_APP_ID = '454751384615998'
FACEBOOK_APP_SECRET = '3ba1e9f1d24bc7af415285e7adacf489' 




