import os

DEBUG = True
PORT = 8007

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, '..', 'media'))

DATA_BASE = {
    'username': 'vir-mir',
    'password': 'rf,fkbcnbrf',
    'host': 'localhost',
    'db': 'exness_comment',
}
