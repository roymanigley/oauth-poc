# OAuth2 POC

## OAuth Server

### Initial
```
python -m venv .venv && source .venv
pip install -r requirements.txt
./manage.py migrate
./manage.py shell < init.py
```

### Run Server
```
./manage.py runserver
```

## OAuth POC

### `authorization_code`

#### Initial
```
cd poc/authorization-code/
python -m venv .venv && source .venv
pip install -r requirements.txt
```

#### Run Server
```
./main.py
```
### `client_credentials`

#### Initial
```
cd poc/client-credentials/
python -m venv .venv && source .venv
pip install -r requirements.txt
```

#### Run Server
```
python main.py
```
