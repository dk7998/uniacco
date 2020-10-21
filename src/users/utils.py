import json
from django.conf import settings

f         = open(settings.BASE_DIR  / 'google_login.json', 'r') 
data      = json.load(f)
CLIENT_ID = data['web']['client_id']

def get_google_client_id():
    return CLIENT_ID