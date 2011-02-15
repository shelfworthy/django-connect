from django.template import RequestContext
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect

from connect import NetworkManager

def get_first(iterable, default=None):
    if iterable:
        return iterable[0]

def disconnect(request, service):
    if request.user.is_anonymous():
        del request.session[service + '_data']
        del request.session[service + '_token']
        return HttpResponseRedirect(reverse('finish_login'))
    else:
        request.member.social.disconnect(service)
        return HttpResponseRedirect(reverse('settings_page', page='connections'))

def connect(request, service, redirect_field_name="next", redirect_to_session_key="redirect_to"):
    access = NetworkManager().get_oauth_access(service)
    
    token = None
    extra = ""
    
    if not service == "facebook":
        token = access.unauthorized_token()
        request.session["%s_unauth_token" % service] = token.to_string()
    elif service == "facebook":
        extra = "&scope=publish_stream,create_event,offline_access,rsvp_event,user_likes,user_location"
        
        # if request.mobile:
        #     extra += "&display=touch"
        
        token = None
    
    if hasattr(request, "session"):
        request.session[redirect_to_session_key] = request.GET.get(redirect_field_name)
    return HttpResponseRedirect(access.authorization_url(token) + extra)

@never_cache
def callback(request, service):
    ctx = RequestContext(request)
    access = NetworkManager().get_oauth_access(service)
    unauth_token = request.session.get("%s_unauth_token" % service, None)
    try:
        auth_token = access.check_token(unauth_token, request.GET)
    except MissingToken:
        ctx.update({"error": "token_missing"})
    else:
        if auth_token:
            return access.callback(request, access, auth_token)
        else:
            # @@@ not nice for OAuth 2
            ctx.update({"error": "token_mismatch"})
    print ctx['error']
