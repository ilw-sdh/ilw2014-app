from flask import *
from flask_oauthlib.client import OAuth
from urllib import urlencode
from collections import defaultdict
import json

import utils

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

def get_airport_infos():
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

@facebook.tokengetter
def get_facebook_token(token=None):
    return session.get('oauth_token')

@app.route("/")
def hello():
    if 'oauth_token' in session:
        return render_template('index.html', me = facebook.get('/me'), airports = get_airport_infos() if 'oauth_token' in session else None)
    else:
        return redirect('/login')

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
    return redirect('/')

@app.route("/show")
def show():
    return render_template('show.html')

if __name__ == "__main__":
    app.debug = True
    app.run()

