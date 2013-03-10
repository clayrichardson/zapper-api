import json

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from zapper.auth import UserAuthentication


@require_http_methods(["GET"])
def login(request):
    authenticated = UserAuthentication()
    if authenticated.is_authenticated(request):
        return HttpResponse(json.dumps('ok'), content_type='application/json')
    else:
        return HttpResponse(json.dumps('fail'), content_type='application/json')
