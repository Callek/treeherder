# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.

"""
WSGI config for webapp project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "webapp.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "treeherder.settings")

try:
    import newrelic.agent
except ImportError:
    newrelic = False

if newrelic:
    newrelic.agent.initialize()

from django.core.wsgi import get_wsgi_application
from treeherder.webapp.whitenoise_custom import CustomWhiteNoise

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application()

# Wrap the Django WSGI app with WhiteNoise so the UI can be served by gunicorn
# in production, avoiding the need for Apache/nginx on Heroku. WhiteNoise will
# serve the Django static files at /static/ and also those in the directory
# referenced by WHITENOISE_ROOT at the site root.
application = CustomWhiteNoise(application)

if newrelic:
    application = newrelic.agent.WSGIApplicationWrapper(application)

# Fix django closing connection to MemCachier after every request:
# https://code.djangoproject.com/ticket/11331
# Remove when https://github.com/django/django/pull/4866 fixed.
from django.core.cache.backends.memcached import BaseMemcachedCache
BaseMemcachedCache.close = lambda self, **kwargs: None
