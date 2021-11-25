from crm_agile.settings.base import *

import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Parse database connection url strings
# like psql://user:pass@127.0.0.1:8458/db
DATABASES = {
    # read os.environ['DATABASE_URL'] and raises
    # ImproperlyConfigured exception if not found
    #
    # The db() method is an alias for db_url().
    'default': env.db()
}

ALLOWED_HOSTS = ['crm-agile.herokuapp.com']
