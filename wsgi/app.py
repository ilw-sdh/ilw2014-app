from flask import *
from flask_oauthlib.client import OAuth
from urllib import urlencode
from urllib2 import urlopen
from collections import defaultdict
from functools import wraps
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
    airports = defaultdict(lambda: { 'score': 0, 'friends': [] }, {})
    for friend in fb.get_decorated_friends():
        friend_airports = utils.around_by_country(friend['current_location']['country'], friend['current_location']['latitude'], friend['current_location']['longitude'])
        for airport in friend_airports:
            airports[airport]['name']  = utils.iata_to_name(airport)
            airports[airport]['score'] += 10 if friend['is_close_friend'] else 1
            airports[airport]['friends'].append(friend)
    if 'EDI' in airports: del airports['EDI']
    return airports

def get_top_airports():
    airports = get_airports()
    airport_tuples = sorted(airports.items(), key=lambda tup: tup[1]['score'], reverse=True)
    return dict(airport_tuples[0:20])

def get_decorated_top_airports():
    airports = get_top_airports()
    for k, v in airports.iteritems():
        try:
            v['quotes'] = skyscanner.find_cheapest_quotes("UK", k)
            v['cheapest_quote'] = reduce(lambda x, y: x if x['MinPrice'] < y['MinPrice'] else y, v['quotes'])
            v['index'] = v['score'] / math.log(v['cheapest_quote']['MinPrice'])
            v['url'] = skyscanner.url_for_journey("UK", k)
        except: pass
    airports = dict((k, v) for k, v in airports.iteritems() if 'quotes' in v and v['quotes'])
    return airports

def get_top_airports_by_index():
    airports = get_decorated_top_airports()
    airport_tuples = sorted(airports.items(), key=lambda tup: tup[1]['index'], reverse=True)
    return dict(airport_tuples[0:6])


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
    return "Index w00t"
    #return render_template('index.html', me = facebook.get('/me'), flights = get_top_flights())

@app.route("/top_flights")
@login_required
def top_flights():
    return json.dumps(get_top_airports_by_index())

@app.route("/")
def hello():
    return render_template('hello.html')

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

@app.route("/home")
def show():
    return render_template('home.html')

@app.route("/main")
def show_main():
    return render_template('main.html')

if __name__ == "__main__":
    app.debug = True
    app.run()

