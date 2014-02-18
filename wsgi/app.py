from flask import Flask, url_for, request
from flask_oauth import OAuth

app = Flask(__name__)
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key="1466224973600976",
    consumer_secret="26960e4d7278e704e103525b338fd8f1",
    request_token_params={'scope': 'email'}
)

@app.route("/")
def hello():
    return "Hello ILWhack 2014!."

@app.route('/login')
def login():
    return facebook.authorize(callback="http://localhost/")

if __name__ == "__main__":
    app.debug = True
    app.config['SECRET_KEY'] = "muchsecret"
    app.run(port = 80)

