import requests
USERNAME = 'OmmPrakashRout'
TOKEN = '1b91f1de98051abd74ec1166f099d0d979e1dab6'
DOMAIN = f'{USERNAME}.pythonanywhere.com'
API_BASE = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/'
HEADERS = {'Authorization': f'Token {TOKEN}'}

wsgi_path = f'/var/www/{DOMAIN.lower().replace(".", "_")}_wsgi.py'
wsgi_content = f"""
import os
import sys

path = '/home/{USERNAME}/Chapter123'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'Chapter123.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
"""
requests.post(f'{API_BASE}files/path{wsgi_path}', headers=HEADERS, files={'content': wsgi_content})
requests.post(f'{API_BASE}webapps/{DOMAIN}/reload/', headers=HEADERS)
