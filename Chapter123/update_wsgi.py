import os
import requests

USERNAME = 'OmmPrakashRout'
TOKEN = '1b91f1de98051abd74ec1166f099d0d979e1dab6'
DOMAIN = f'{USERNAME}.pythonanywhere.com'
API_BASE = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/'
HEADERS = {'Authorization': f'Token {TOKEN}'}

wsgi_path = f'/var/www/{DOMAIN.lower().replace(".", "_")}_wsgi.py'

django_wsgi = '''
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chapter123.settings')
application = get_wsgi_application()
'''

print('Uploading proper Django WSGI...')
resp = requests.post(f"{API_BASE}files/path{wsgi_path}", headers=HEADERS, files={'content': django_wsgi})
print('Response status:', resp.status_code)
print('Reloading webapp...')
reload_resp = requests.post(f"{API_BASE}webapps/{DOMAIN}/reload/", headers=HEADERS)
print('Reload response:', reload_resp.status_code)
