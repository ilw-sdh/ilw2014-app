from flask import *
from urllib import urlencode
from urllib2 import urlopen

# Runs a fql query (using urlopen because the oauth thing was being annoying)
def fql(q):
    print session.get('oauth_token')
    query = { 'q': q, 'access_token': session.get('oauth_token')[0] }
    raw = urlopen("https://graph.facebook.com/fql?" + urlencode(query)).read()
    return json.loads(raw)['data']

def get_friends():
    friends = fql('SELECT uid, name, pic, current_location.latitude, current_location.longitude, current_location.country, current_location.city FROM user  WHERE uid IN (SELECT uid2 FROM friend WHERE uid1=me()) AND current_location')    
    return friends

def get_close_friend_ids():
    close_friends = fql("SELECT uid FROM friendlist_member WHERE flid IN (SELECT flid FROM friendlist WHERE owner = me() AND type = 'close_friends')")
    return map(lambda f: f['uid'], close_friends)

def get_decorated_friends():
    friends = get_friends()
    close_friends = get_close_friend_ids()
    for f in friends:
        f['is_close_friend'] = f['uid'] in close_friends
    return friends