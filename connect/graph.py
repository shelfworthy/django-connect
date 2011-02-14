import re
import urllib

from django.utils import simplejson as json

from elsewhere.models import SocialNetwork

def get_connections(urls):
    lookup_url = 'http://socialgraph.apis.google.com/lookup?q=%s&fme=1&edo=1&edi=1' % ','.join(urls)
    info_from_google = json.loads(urllib.urlopen(lookup_url).read())

    nodes = info_from_google['nodes']

    claimed_nodes = []
    unverified_claiming_nodes = []
    nodes_referenced = []
    nodes_referenced_by = []

    for node in nodes.values():
        claimed_nodes = claimed_nodes + node['claimed_nodes']
        unverified_claiming_nodes = unverified_claiming_nodes + node['unverified_claiming_nodes']

        # for key in node['nodes_referenced'].keys():
        #     if 'me' in node['nodes_referenced'][key]['types']:
        #         nodes_referenced.append(key)
        # 
        # for key in node['nodes_referenced_by'].keys():
        #     if 'me' in node['nodes_referenced_by'][key]['types']:
        #         nodes_referenced.append(key)

    all_nodes = claimed_nodes + unverified_claiming_nodes + nodes_referenced + nodes_referenced_by

    all_networks = list(SocialNetwork.objects.all().only('url'))

    final_list = []

    for item in all_nodes:
        for network in all_networks:
            if re.match(network.url % '[\w-]+', item):
                final_list.append(item)

    return final_list

# http://pownce.com/[\w-]+/something

# def get_friends_from_twitter(username):
#     usernames = []
#     members = []
#     base_url = 'http://twitter.com/statuses/friends/%s.json' % username
#     friends_from_twitter = json.loads(urllib.urlopen(base_url).read())
# 
#     if friends_from_twitter:
#         for friend in friends_from_twitter:
#             usernames.append(friend['screen_name'])
#         i = 2
#         while friends_from_twitter:
#             friends_from_twitter = json.loads(urllib.urlopen(base_url + '?page=%s' % i).read())
#             i += 1
#             for friend in friends_from_twitter:
#                 usernames.append(friend['screen_name'])
# 
#         for name in usernames:
#             try:
#                 members.append(Member.objects.get(user__username=name, is_enabled=True))
#             except Member.DoesNotExist:
#                 pass
#         return members
#     else:
#         return None
# 