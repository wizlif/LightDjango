import os
import sys

import simplejson as simplejson
from django.conf import settings

DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', '{{ secret_key }}')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)

from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse

import couchdb

couchserver = couchdb.Server("http://localhost:5984/")

dbname = "ezyextension"
db = None

if dbname in couchserver:
    db = couchserver[dbname]


def index(request):
    return HttpResponse('Hello World')


def ordersV1(request):
    if request.method == 'GET':
        data = []
        for x in db.view('orders/order_total', include_docs=True):
            data.append(x["doc"])
        data = simplejson.dumps(data)
        return HttpResponse(data, content_type='application/json')

    elif request.method == 'POST':
        data = []
        for x in db.view('orders/all', include_docs=True):
            data.append(x["doc"])
        data = simplejson.dumps(data)
        return HttpResponse(data, content_type='application/json')


urlpatterns = (
    url(r'^$', index),
    url(r'^api/v1/orders', ordersV1),
)

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
