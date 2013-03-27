from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template import RequestContext

@ensure_csrf_cookie
def landing_page(request):
    return render_to_response('landing.html', {}, RequestContext(request))

@ensure_csrf_cookie
def yc_landing_page(request):
    return render_to_response('yc_landing.html', {}, RequestContext(request))

