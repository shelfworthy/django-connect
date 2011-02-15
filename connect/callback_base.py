#Common imports for social callbacks
#TODO: refactor this

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

REDIRECT_BACK_TO = '/' #reverse('settings_page', kwargs={'page': 'connections'})