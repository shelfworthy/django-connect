import urllib

from django.utils import simplejson as json

def get_connections(urls):
    lookup_url = 'http://socialgraph.apis.google.com/lookup?q=%s&fme=1&edo=1&edi=1' % ','.join(urls)
    info_from_google = json.loads(urllib.urlopen(lookup_url).read())

    return info_from_google

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