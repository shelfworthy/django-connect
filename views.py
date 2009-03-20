from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from connect.functions import get_connections

def list(request):
    connections = get_connections(['chrisdrackett.com',])


    return render_to_response(
        'connect/list.html',
        {'connections': connections,},
        context_instance=RequestContext(request))