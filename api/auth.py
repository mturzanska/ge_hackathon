from os import getenv
import json

import requests

CLIENT_CREDS = getenv('base64ClientCredential', '')


class AuthenticatorFactory(object):
    def __init__(self, client_id, zone_id, b64cred, auth_endpoint):
        self.client_id = client_id
        self.zone_id = zone_id
        self.b64cred = b64cred
        self.auth_endpoint = auth_endpoint
        self.token = None

    def set_token(self):
        headers = {
            'authorization': 'Basic {b64cred}'.format(b64cred=self.b64cred),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': self.client_id,
            'grant_type': 'client_credentials'
        }
        rsp = requests.post(self.auth_endpoint, headers=headers, data=data)
        if rsp.status_code == 200:
            self.token = json.loads(rsp.text)['access_token']
        # raise error if bad request

    def create_authenticator(self):
        if self.token is None:
            self.set_token()
        return PredixAuth(self.token, self.zone_id)


class PredixAuth(requests.auth.AuthBase):
    def __init__(self, token, zone_id):
        self.token = token
        self.zone_id = zone_id

    def __call__(self, r):
        r.headers['Authorization'] = 'bearer {token}'.format(token=self.token)
        r.headers['predix-zone-id'] = self.zone_id
        return r
