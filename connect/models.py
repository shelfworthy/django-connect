from django.db import models
from django.conf import settings

from oauth_access.access import OAuthAccess
from oauth_access.models import UserAssociation

from connect import NetworkManager

class SocialManager(object):
    def __init__(self, user):
        self.user = user
    
    def get(self, network):
        try:
            data = self.user.userassociation_set.get(service=network)
            return NetworkManager().get_user(network, data.token)
        except UserAssociation.DoesNotExist:
            return NetworkManager().get_user(network, member=self.member)
    
    def create(self, service, token):
        pass
    
    def list_connected(self, network):
        return [NetworkManager().get_user(x.service, x.token) for x in self.user.userassociation_set.all()]
    
    def is_connected(self, network):
        if "connectable" in NetworkManager().get(network).support:
            return self.user.userassociation_set.filter(service=network).exists()
        else:
            return True
    
    def disconnect(self, service):
        self.user.userassociation_set.filter(service=service).delete()