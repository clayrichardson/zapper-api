
from django.http import HttpResponse

import logging
logger = logging.getLogger(__name__)

class HttpFound(HttpResponse):
    status_code = 302

