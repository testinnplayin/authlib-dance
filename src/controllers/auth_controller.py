import json

from authlib.integrations.httpx_client import AsyncOAuth2Client
from flask import Flask, redirect, render_template, request


class AuthController:
    def __init__(self):
        self.client_id = ''
        self.client_secret = ''
        self.client = {}
        self.state = ''

    def authorize(self, auth_url):
        if str(request.query_string, 'utf-8') == 'api=gh':
            config_info = self._opener()
            self.redirection_url = config_info['redirection_url']
            self.client_id = config_info['client_id']
            self.client_secret = config_info['client_secret']

            redirect_uri = f'{self.redirection_url}/test'

            self.client = AsyncOAuth2Client(
                self.client_id, self.client_secret, redirect_uri=redirect_uri)

            uri, state = self.client.create_authorization_url(auth_url)
            print('uri ', uri)
            print('state ', state)
            return redirect(uri)

    def get_client(self):
        return self.client

    def _opener(self):
        with open('../../config.json', 'r') as f:
            f_json = f.read()
        f_info = json.loads(f_json)
        return f_info
