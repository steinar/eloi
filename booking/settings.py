import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = '%s/eloi.db' % BASE_PATH

SERVER_PORT = 8100

UPLOADS_DEFAULT_DEST = '%s/eloi/static/data' % BASE_PATH
UPLOADS_DEFAULT_URL = '/static/data/'