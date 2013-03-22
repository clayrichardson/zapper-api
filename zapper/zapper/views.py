from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def landing_page(request):
    return render_to_response('landing.html', {})
