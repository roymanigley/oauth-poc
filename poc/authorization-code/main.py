#!/usr/bin/env python3
import random
import string
import hashlib
import base64
import requests
from constants import Constants
from requests.auth import HTTPBasicAuth
from cryptography.fernet import Fernet

from flask import Flask, request, render_template

app = Flask('OAuth2 POC')


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
            auth=HTTPBasicAuth(
                Constants.CLIENT_ID_AUTHORIZATION_CODE,
                Constants.CLIENT_SECRET_AUTHORIZATION_CODE
            ),
            data=data,
        )
        response_tenant = requests.get(
            url=f'{Constants.API_BASE_URL}/api/tenants/current_tennant/',
            headers={
                'Authorization': f'Bearer {response.json()["access_token"]}'
            }
        )
        print(response_tenant.status_code, response_tenant.json())
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
            'client_id': Constants.CLIENT_ID_AUTHORIZATION_CODE,
            'redirect_uri': Constants.REDIRECT_URI,
            'scope': '+'.join(Constants.SCOPES),
        }

        return f'{Constants.AUTHORIZATION_BASE_URL}?{"&".join([f"{key}={value}" for key, value in auth_params.items()])}'


if __name__ == '__main__':
    app.run()
