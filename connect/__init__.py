import os

from django.utils.importlib import import_module
from django.conf import settings

from oauth_access.access import OAuthAccess

class NetworkManager(object):
    _networks = None
    
    def __init__(self):
        self._load_networks()
    
    def _load_networks(self):
        if not self._networks:
            _networks = {}
            command_dir = os.path.join(__path__[0], 'networks')
            
            modules = [f[:-3] for f in os.listdir(command_dir)
                    if not f.startswith('_') and f.endswith('.py')]
            
            for module in modules:
                _networks[module] = getattr(import_module(__package__ + '.networks.' + module), 'SocialBackend')
        
        self._networks = _networks
    
    def filter(self, feature):
        return dict([x for x in self._networks.items() if feature in x[1].support])
    
    def profile_picture(self):
        return self.filter('profile_picture')
    
    def post(self):
        return self.filter('post')
    
    def auth(self):
        return self.filter('auth')
    
    def connect_list(self):
        return self.filter('connectable')
    
    def all(self):
        return self._networks
    
    def get(self, network, member=None):
        network = self._networks[network]
        if member:
            return network(member)
        return network
        
    def get_oauth_access(self, network):
        return OAuthAccess(network, 
            settings.OAUTH_ACCESS_SETTINGS[network]['keys']['KEY'],
            settings.OAUTH_ACCESS_SETTINGS[network]['keys']['SECRET'],
            self.get(network).endpoints,
            self.get(network).callback
            )
            
    def get_user(self, network, auth_token=None, data=None, member=None):
        if auth_token:
            return self.get(network)(self.get_oauth_access(network), auth_token, data)
        elif member:
            return self.get(network, member)
