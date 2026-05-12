import requests
import time

USERNAME = 'OmmPrakashRout'
TOKEN = '1b91f1de98051abd74ec1166f099d0d979e1dab6'
DOMAIN = f'{USERNAME}.pythonanywhere.com'
API_BASE = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/'
HEADERS = {'Authorization': f'Token {TOKEN}'}

wsgi_path = f'/var/www/{DOMAIN.lower().replace(".", "_")}_wsgi.py'

extraction_wsgi = '''
import zipfile
import os
import subprocess

def extract():
    with zipfile.ZipFile("/home/OmmPrakashRout/Chapter123.zip", "r") as zip_ref:
        zip_ref.extractall("/home/OmmPrakashRout/Chapter123")
    subprocess.check_call(["pip3.10", "install", "django", "--user"])
    subprocess.check_call(["python3.10", "/home/OmmPrakashRout/Chapter123/manage.py", "migrate"])

try:
    extract()
except Exception as e:
    with open("/home/OmmPrakashRout/deploy_error.txt", "w") as f:
        f.write(str(e))

def application(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"Extraction WSGI finished!"]
'''

print("Uploading extraction WSGI...")
requests.post(f'{API_BASE}files/path{wsgi_path}', headers=HEADERS, files={'content': extraction_wsgi})
print("Reloading webapp...")
requests.post(f'{API_BASE}webapps/{DOMAIN}/reload/', headers=HEADERS)

print("Triggering extraction by visiting the domain...")
try:
    print(requests.get(f'http://{DOMAIN}', timeout=30).text)
except requests.exceptions.ReadTimeout:
    print("Request timed out, but extraction might have completed.")
