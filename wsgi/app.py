from flask import *
from flask_oauthlib.client import OAuth
from urllib import urlencode
from urllib2 import urlopen
from collections import defaultdict
from functools import wraps
from sets import Set
import json
import random
import math

import utils
import skyscanner
import facebook as fb

app = Flask(__name__)
app.secret_key = "muchsecret"
oauth = OAuth(app)

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key="1466224973600976",
    consumer_secret="26960e4d7278e704e103525b338fd8f1",
    request_token_params={'scope': 'email,friends_location,user_location,read_friendlists'}
)


@facebook.tokengetter
def get_facebook_token(token=None):
    return session.get('oauth_token')

def get_airports():
    airports = defaultdict(lambda: { 'friend_score': 0, 'friends': [] }, {})
    for friend in fb.get_decorated_friends():
        friend_airports = utils.around_by_country(friend['current_location']['country'], friend['current_location']['latitude'], friend['current_location']['longitude'])
        for airport in friend_airports:
            airports[airport]['name']  = utils.iata_to_name(airport)
            airports[airport]['friend_score'] += 10 if friend['is_close_friend'] else 1
            airports[airport]['friends'].append(friend)
            airports[airport]['iata'] = airport
            #airports[airport]['quotes'] = skyscanner.find_cheapest_quotes("UK", airport)
    if 'EDI' in airports: del airports['EDI']
    return airports

def get_friends():
    friends = {}
    for k, v in get_decorated_top_airports().iteritems():
        for f in v['friends']:
            cheapest_quote = v['cheapest_quote']
            if f['uid'] in friends:
                if cheapest_quote['MinPrice'] < friends[f['uid']]['cheapest_quote']['MinPrice']:
                    friends[f['uid']]['cheapest_quote'] = cheapest_quote
            else:
                friends[f['uid']] = f
                friends[f['uid']]['cheapest_quote'] = cheapest_quote
    return friends.values()

def get_top_airports():
    airports = get_airports()
    airport_tuples = sorted(airports.items(), key=lambda tup: tup[1]['friend_score'], reverse=True)
    return dict(airport_tuples[0:20])

def get_decorated_top_airports():
    airports = get_top_airports()
    for k, v in airports.iteritems():
        try:
            v['quotes'] = skyscanner.find_cheapest_quotes("edi", k)
            v['cheapest_quote'] = reduce(lambda x, y: x if x['MinPrice'] < y['MinPrice'] else y, v['quotes'])
            v['index'] = v['friend_score'] # / math.log(v['cheapest_quote']['MinPrice'])
            v['url'] = skyscanner.url_for_journey("edi", k)
        except: pass
    airports = dict((k, v) for k, v in airports.iteritems() if 'quotes' in v and v['quotes'])
    return airports

def get_top_airports_by_index():
    airports = get_decorated_top_airports()
    airport_tuples = sorted(airports.items(), key=lambda tup: tup[1]['index'], reverse=True)
    return map(lambda x: x[1], airport_tuples[0:6])


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not ('oauth_token' in session):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/index")
@login_required
def index():
    #return "Index w00t"
    #return render_template('main.html', me = facebook.get('/me'), flights = get_top_flights())
    return render_template('main.html', friends = fb.get_decorated_friends())

@app.route("/top_flights")
@login_required
def top_flights():
    return json.dumps(get_top_airports_by_index(), indent=4)

@app.route("/friend_flights")
@login_required
def friend_flights():
    try:
        country, lat, lon = request.args['country'], float(request.args['lat']), float(request.args['lon'])
        airports_codes = utils.around_by_country(country, lat, lon)

        airports = defaultdict(lambda: {}, {})
        for k in airports_codes:
            try:
                airports[k]['quotes'] = skyscanner.find_cheapest_quotes("edi", k)
                airports[k]['name']  = utils.iata_to_name(k)
                airports[k]['cheapest_quote'] = reduce(lambda x, y: x if x['MinPrice'] < y['MinPrice'] else y, airports[k]['quotes'])
                airports[k]['url'] = skyscanner.url_for_journey("edi", k)
                airports[k]['iata'] = k
            except: pass

        if len(airports) == 0:
            return json.dumps({ 'result': None }, indent=4)
        else:
            best_airport = reduce(lambda x, y: x if x['cheapest_quote']['MinPrice'] < y['cheapest_quote']['MinPrice'] else y, airports.values())
            return json.dumps({ 'result': best_airport }, indent=4)
    except:
        return json.dumps({ 'result': None }, indent=4)

@app.route("/")
def hello():
    if not ('oauth_token' in session):
        return render_template('home.html')
    else:
        return redirect('/index')

@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@app.route("/logout")
def logout():
    facebook.delete('/me/permissions')
    del session['oauth_token']
    return redirect('/')

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.debug = True
    app.run()
