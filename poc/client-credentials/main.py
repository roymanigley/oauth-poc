#!/usr/bin/env python3
from constants import Constants
import requests


class Client:

    @staticmethod
    def fetch_tokens():
        data = {
            "grant_type": "client_credentials",
            "scope": ' '.join(Constants.SCOPES),
        }

        response = requests.post(
            url=Constants.TOKEN_BASE_URL,
            data=data,
            auth=(
                Constants.CLIENT_ID_CLIENT_CREDENTIALS,
                Constants.CLIENT_SECRET_CLIENT_CREDENTIALS
            ),
        )

        if response.status_code == 200:
            token_info = response.json()
            access_token = token_info.get("access_token")
            print("Access Token:", access_token)
            response = requests.get(
                url=f'{Constants.API_BASE_URL}/api/tenants/current_tennant/',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            print(response.status_code, response.json())
        else:
            print("Failed to get token:", response.status_code, response.text)


if __name__ == '__main__':
    Client.fetch_tokens()
