import hashlib
from urllib import urlencode

from django.conf import settings

from connect.networks import BaseSocialBackend


class SocialBackend(BaseSocialBackend):
    support = ["profile_picture"]
    name = "gravatar"
    display_name = "Gravatar"
    
    def __init__(self, member):
        self.member = member
        
    def _get_profile_picture_url(self, size):
        if size == 'small':
            default = self.member.default_profile_picture_url_small
            image_size = 50
        else:
            default = self.member.default_profile_picture_url_large
            image_size = 100
        
        return "http://www.gravatar.com/avatar.php?" + urlencode({
            'gravatar_id':  hashlib.md5(self.member.email.strip().lower()).hexdigest(),
            'default':      default,
            'size':         image_size
        })
    
    def get_profile_picture_url_small(self):
        return self._get_profile_picture_url('small')
    
    def get_profile_picture_url_large(self):
        return self._get_profile_picture_url('large')