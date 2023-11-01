from . import tasks
from . import media
from . import collections

class EdenTaskFailedError(Exception):
    pass

api_url = "https://api.eden.art"
api_key = None
api_secret = None

poll_interval = 5
timeout = 3600
verbose = False

import os
from dotenv import load_dotenv

load_dotenv()

if 'EDEN_API_KEY' in os.environ:
    api_key = os.environ['EDEN_API_KEY']
if 'EDEN_API_SECRET' in os.environ:
    api_secret = os.environ['EDEN_API_SECRET']
if 'EDEN_API_URL' in os.environ:
    api_url = os.environ['EDEN_API_URL']
