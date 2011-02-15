#Basic interface class for all backends

class BaseSocialBackend(object):
    name = "network"
    display_name = "Network Needs A Name"
    
    support = []
    
    def __init__(self, access=None, auth_token=None, data=None):
        self.access = access
        self.auth_token = auth_token
        
        if data:
            self.data = data
        else:
            self._init_data()
    
    def _init_data(self):
        self.data = self.access.make_api_call("json", self.endpoints['data'], self.auth_token) 
        
    def persist(self, user=None):
        self.access.persist(user, self.auth_token, self.user_id())
    
    def get_email(self):
        raise NotImplementedError
    
    def get_username(self):
        raise NotImplementedError
    
    def get_service_username(self):
        # Username formatted in the manner in which the service formats it.
        return self.get_username()
    
    def get_profile_picture_url_small(self):
        # this should return a url for an image at 50x50 pixels.
        raise NotImplementedError

    def get_profile_picture_url_large(self):
        # this should return a url for an image at 100x100 pixels.
        raise NotImplementedError
    
    def callback(request, access, token):
        raise NotImplementedError
    
    def connect_user(self, member):
        raise NotImplementedError
    
    def post_message(self, message):
        raise NotImplementedError
    
    def post_event(self, message):
        raise NotImplementedError
    
    def get_profile_url(self):
        raise NotImplementedError
    
    def get_display_name(self):
        raise NotImplementedError
    
    def are_friends(self, friend):
        raise NotImplementedError
    
    def follow(self, friend):
        raise NotImplementedError
    
    def unfollow(self, friend):
        raise NotImplementedError
        
    def user_id(self):
        raise NotImplementedError
    
    def is_supported(self, feature):
        return (feature in self.support)
