from . import tasks
from . import media

class EdenTaskFailedError(Exception):
    pass

api_url = "https://api.eden.art"
api_key = None
api_secret = None

poll_interval = 5
timeout = 3600
verbose = False
