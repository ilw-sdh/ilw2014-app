from flask import *
from flask_oauthlib.client import OAuth

from utils import geocalc

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
    request_token_params={'scope': 'email'}
)

@facebook.tokengetter
def get_facebook_token(token=None):
    return session.get('oauth_token')

@app.route("/")
def hello():
    return render_template('index.html', me = facebook.get('/me') if 'oauth_token' in session else None)

@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

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

if __name__ == "__main__":
    app.debug = True
    app.run()

