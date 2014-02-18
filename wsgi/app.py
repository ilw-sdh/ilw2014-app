from flask import *
from flask_oauthlib.client import OAuth
from urllib import urlencode
from collections import defaultdict
from functools import wraps
import json

import utils
import skyscanner

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
    request_token_params={'scope': 'email,friends_location'}
)

def get_airports():
    airports = defaultdict(lambda: { 'score': 0, 'friends': [] }, {})
    query = { 'q': 'SELECT name, current_location.latitude, current_location.longitude FROM user  WHERE uid IN (SELECT uid2 FROM friend WHERE uid1=me()) AND current_location' }
    friends = facebook.get('/fql?' + urlencode(query)).data
    for friend in friends['data']:
        friend_airports = utils.around(friend['current_location']['latitude'], friend['current_location']['longitude'])
        for airport in friend_airports:
            airports[airport]['name']  = utils.iata_to_name(airport)
            airports[airport]['score'] += 1
            airports[airport]['friends'].append(friend['name'])
    return airports

def get_top_airports(n):
    airports = get_airports()
    query = { 'q': 'SELECT current_location.latitude, current_location.longitude FROM user WHERE uid = me()' }
    my_location = facebook.get('/fql?' + urlencode(query)).data['data'][0]['current_location']
    my_airports = utils.around(my_location['latitude'], my_location['longitude'])
    for x in my_airports:
        del airports[x]
    airport_tuples = sorted(airports.items(), key=lambda tup: tup[1]['score'], reverse=True)
    airports = dict(airport_tuples[0:n])
    for k, v in airports.iteritems():
        v['prices'] = []
        for x in my_airports:
            try:
                v['prices'].append(skyscanner.find_best_quote("LON", json.loads(k))['MinPrice'])
            except: pass
    airports = dict((k, v) for k, v in airports.iteritems() if v['prices'])
    return airports

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not ('oauth_token' in session):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@facebook.tokengetter
def get_facebook_token(token=None):
    return session.get('oauth_token')

@app.route("/index")
@login_required
def index():
    return render_template('index.html', me = facebook.get('/me'), airports = get_top_airports(10))

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

@app.route("/show")
def show():
    return render_template('show.html')

if __name__ == "__main__":
    app.debug = True
    app.run()

