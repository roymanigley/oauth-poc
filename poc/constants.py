import os


class Constants:
    FERNET_KEY = os.environ.get(
        'POC_FERNET_KEY', 'LVpHbm5RbGdvSXMwd3dUU1V5RFhvVDBtc0lyQXc3b0JnZkZmOEV2RnNBQT0='
    )
    CLIENT_ID_AUTHORIZATION_CODE = os.environ.get(
        'POC_CLIENT_ID_AUTHORIZATION_CODE', 'poc-authorization'
    )
    CLIENT_SECRET_AUTHORIZATION_CODE = os.environ.get(
        'POC_CLIENT_SECRET_AUTHORIZATION_CODE', 'super-secret'
    )
    CLIENT_ID_CLIENT_CREDENTIALS = os.environ.get(
        'POC_CLIENT_ID_CLIENT_CREDENTIALS', 'poc-client-credential'
    )
    CLIENT_SECRET_CLIENT_CREDENTIALS = os.environ.get(
        'POC_CLIENT_SECRET_CLIENT_CREDENTIALS', 'super-secret'
    )
    REDIRECT_URI = os.environ.get(
        'POC_REDIRECT_URI', 'http://127.0.0.1:5000/callback/'
    )
    SCOPES = os.environ.get(
        'POC_SCOPES', 'create read update delete openid'
    ).split(' ')
    AUTHORIZATION_BASE_URL = os.environ.get(
        'POC_AUTHORIZATION_BASE_URL', 'http://localhost:8000/oauth/authorize/'
    )
    TOKEN_BASE_URL = os.environ.get(
        'POC_TOKEN_BASE_URL', 'http://localhost:8000/oauth/token/'
    )
    API_BASE_URL = os.environ.get(
        'POC_API_BASE_URL', 'http://localhost:8000/'
    )
