from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login

from zapper.errors import Errors

Errors = Errors.Errors

def error_handle(error):
    return HttpResponse(
        simplejson.dumps({'error': error}),
        mimetype='application/json'
    )

def check_login(request):
    if request.user.is_authenticated():
        return home(request)
    else:
        c = {}
        c.update(csrf(request))
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('ok')
                else:
                    return error_handle(Errors.INVALID_ACCOUNT)
            else:
                return error_handle(Errors.INVALID_LOGIN)
        else:
            return render_to_response('landing.html', c)

def home(request):
    return render_to_response('index.html', {})
