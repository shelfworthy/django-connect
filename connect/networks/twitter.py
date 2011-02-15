from connect.networks import BaseSocialBackend
from connect.callback_base import *

class SocialBackend(BaseSocialBackend):
    endpoints = {
        "request_token": "https://twitter.com/oauth/request_token",
        "access_token": "https://twitter.com/oauth/access_token",
        "authorize": "http://twitter.com/oauth/authenticate",
        "data": "https://twitter.com/account/verify_credentials.json",
        "post": "http://api.twitter.com/1/statuses/update.json", 
    }
    support = ["connectable", "post", "search_friends", "profile_picture", "auth"]
    name = "twitter"
    display_name = "Twitter"
    
    def get_username(self):
        return self.data['screen_name']
    
    def get_service_username(self):
        return "@%s" % self.get_username()
    
    def get_email(self):
        return ''
    
    def get_profile_picture_url_small(self):
        # using http://img.tweetimag.es/
        return "http://img.tweetimag.es/i/%s_%s" % (self.get_username(), 'n')
    
    def get_profile_picture_url_large(self):
        # using http://img.tweetimag.es/ this image is 73x73, but thats the best twitter can muster.
        return "http://img.tweetimag.es/i/%s_%s" % (self.get_username(), 'b')
    
    def post(self, status):
        self.access.make_api_call("json", self.post_url, self.auth_token, method="POST", body={'status':status})
    
    def user_id(self):
        return self.data['id']
    
    @staticmethod
    def callback(request, access, token):
        url = "https://twitter.com/account/verify_credentials.json"
        user_data = access.make_api_call("json", url, token)
        user = access.lookup_user(identifier=user_data["id"])
        
        if not request.user.is_authenticated():
            if user is None:
                request.session['twitter_data'] = user_data
                request.session['twitter_token'] = token
                return redirect(reverse('finish_login'))
                # user = User.objects.create_user(user_data["screen_name"], user_data.get("email", ''))
                
                
            
            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)
            access.persist(user, token, identifier=user_data["id"])
            return redirect('/')
        else:
            user = request.user
        
        access.persist(user, token, identifier=user_data["id"])
        return redirect(REDIRECT_BACK_TO)
