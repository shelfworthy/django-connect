from connect.networks import BaseSocialBackend
from connect.callback_base import *

class SocialBackend(BaseSocialBackend):
    endpoints = {
        # OAuth 2.0 does not need a request token
        "access_token": "https://graph.facebook.com/oauth/access_token",
        "authorize": "https://graph.facebook.com/oauth/authorize",
        "data": "https://graph.facebook.com/me"
    }
    support = ["connectable", "post", "search_friends", "profile_picture", "auth"]
    name = "facebook"
    display_name = "Facebook"
    
    def _init_data(self):
        from oauth_access.access import OAuth20Token
        self.data = self.access.make_api_call("json", self.endpoints['data'], OAuth20Token(self.auth_token)) 
    
    def get_username(self):
        return self.data['name']
    
    def get_email(self):
        return self.data.get('email')
    
    def get_profile_picture_url_small(self):
        return 'https://graph.facebook.com/%s/picture' % self.data['id']
    
    def get_profile_picture_url_large(self):
        # this image isn't a square, so it might not be worth using.
        return 'https://graph.facebook.com/%s/picture?type=normal' % self.data['id']
    
    def user_id(self):
        return self.data['id']

    @staticmethod
    def callback(request, access, token):
        url = "https://graph.facebook.com/me"
        user_data = access.make_api_call("json", url, token)
        user = access.lookup_user(identifier=user_data["id"])
        
        if not request.user.is_authenticated():
            if user is None:
                request.session['facebook_data'] = user_data
                request.session['facebook_token'] = token
                
                #hack usernames
                if not 'profile.php?id=' in user_data['link']:
                    user_data['name'] = user_data['link'].split('/')[-1]
                
                return redirect(reverse('finish_login'))

            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)
            access.persist(user, token, identifier=user_data["id"])
            return redirect('/')
        else:
            user = request.user

        access.persist(user, token, identifier=user_data["id"])
        return redirect(REDIRECT_BACK_TO)



