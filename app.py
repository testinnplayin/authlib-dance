import json

from authlib.integrations.requests_client import OAuth2Session
from flask import Flask, redirect, render_template, request


app = Flask(__name__)


def opener() -> dict:
    with open('./config.json', 'r') as f:
        f_json = f.read()
    f_info = json.loads(f_json)
    return f_info

config_info = opener()
redirection_url = config_info['redirection_url']
client_id = config_info['client_id']
client_secret = config_info['client_secret']

redirect_uri = f'{redirection_url}/test'


client = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)
state = ''


@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/authorize', methods=['POST'])
def authorize():
    github_auth_url = 'https://github.com/login/oauth/authorize'
    
    if request.args.get('api') == 'gh':
        github_auth_url = 'https://github.com/login/oauth/authorize'

        uri, state = client.create_authorization_url(github_auth_url)
        print('uri ', uri)
        return redirect(uri)


@app.route('/test')
def get_token():
    token_url = f'https://github.com/login/oauth/access_token'
    token = client.fetch_token(token_url, authorization_response=request.url)
    print('token ', token)
    return 'Success'
