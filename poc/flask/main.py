import random
import string
import hashlib
import base64
import requests
import os
from requests.auth import HTTPBasicAuth
from cryptography.fernet import Fernet

from flask import Flask, request, render_template

app = Flask('OAuth2 POC')


class Constants:
    FERNET_KEY = os.environ.get(
        'FERNET_KEY', 'LVpHbm5RbGdvSXMwd3dUU1V5RFhvVDBtc0lyQXc3b0JnZkZmOEV2RnNBQT0='
    )
    CLIENT_ID = os.environ.get(
        'CLIENT_ID', 'poc-authorization'
    )
    CLIENT_SECRET = os.environ.get(
        'CLIENT_SECRET', 'super-secret'
    )
    REDIRECT_URI = os.environ.get(
        'REDIRECT_URI', 'http://127.0.0.1:5000/callback/'
    )
    SCOPES = os.environ.get(
        'SCOPES', 'create read update delete openid'
    ).split(' ')
    AUTHORIZATION_BASE_URL = os.environ.get(
        'AUTHORIZATION_BASE_URL', 'https://oauth-royman.leapcell.app/oauth/authorize/'
    )
    TOKEN_BASE_URL = os.environ.get(
        'TOKEN_BASE_URL', 'https://oauth-royman.leapcell.app/oauth/token/'
    )


class API:

    @app.get('/')
    def home():
        return render_template(
            'login.html',
            **{
                'authorization_url': Utils.get_authorization_url()
            }
        )

    @app.get('/callback/')
    def callback():
        state = request.args.get('state', '')
        state_decrypted = Utils.decrypt(Constants.FERNET_KEY, state)
        code = request.args.get('code', '')
        data = {
            "grant_type": "authorization_code",
            "redirect_uri": Constants.REDIRECT_URI,
            "code": code,
            "code_verifier": state_decrypted,
        }
        response = requests.post(
            url=Constants.TOKEN_BASE_URL,
            auth=HTTPBasicAuth(Constants.CLIENT_ID, Constants.CLIENT_SECRET),
            data=data,
        )
        return response.json()


class Utils:
    @staticmethod
    def get_verifier() -> str:
        return ''.join(
            random.choice(
                string.ascii_uppercase + string.digits
            ) for _ in range(random.randint(43, 128))
        )

    @staticmethod
    def get_codechallenge(code_verifier) -> str:
        code_challenge = hashlib.sha256(
            code_verifier.encode('utf-8')
        ).digest()

        return base64.urlsafe_b64encode(
            code_challenge
        ).decode('utf-8').replace('=', '')

    @staticmethod
    def encrypt(key: str, data: str) -> str:
        key_encoded = base64.decodebytes(key.encode('utf-8'))
        return base64.urlsafe_b64encode(
            Fernet(key=key_encoded).encrypt(data=data.encode('utf-8'))
        ).decode('utf-8')

    @staticmethod
    def decrypt(key: str, data: str) -> str:
        key_encoded = base64.decodebytes(key.encode('utf-8'))
        return Fernet(key=key_encoded).decrypt(
            token=base64.urlsafe_b64decode(data)
        ).decode('utf-8')

    @staticmethod
    def get_authorization_url() -> str:
        verifier = Utils.get_verifier()
        code_challange = Utils.get_codechallenge(verifier)
        state = Utils.encrypt(Constants.FERNET_KEY, verifier)
        auth_params = {
            'response_type': 'code',
            'code_challenge': code_challange,
            'state': state,
            'code_challenge_method': 'S256',
            'client_id': Constants.CLIENT_ID,
            'redirect_uri': Constants.REDIRECT_URI,
            'scope': '+'.join(Constants.SCOPES),
        }

        return f'{Constants.AUTHORIZATION_BASE_URL}?{"&".join([f"{key}={value}" for key, value in auth_params.items()])}'


if __name__ == '__main__':
    app.run()
