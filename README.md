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

## OAuth Flask Client

### Initial
```
cd poc/flask/
python -m venv .venv && source .venv
pip install -r requirements.txt
```

### Run Server
```
python main.py
```
