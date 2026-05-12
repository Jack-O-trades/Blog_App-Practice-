import requests
USERNAME = 'OmmPrakashRout'
TOKEN = '1b91f1de98051abd74ec1166f099d0d979e1dab6'
DOMAIN = f'{USERNAME}.pythonanywhere.com'
API_BASE = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/'
HEADERS = {'Authorization': f'Token {TOKEN}'}

log_path = f'/var/log/{DOMAIN.lower()}.error.log'
url = f'{API_BASE}files/path{log_path}'

response = requests.get(url, headers=HEADERS)
if response.status_code == 200:
    print(response.text[-2000:]) # Print last 2000 characters
else:
    print(f"Failed to fetch logs: {response.status_code} - {response.text}")

server_log_path = f'/var/log/{DOMAIN.lower()}.server.log'
server_url = f'{API_BASE}files/path{server_log_path}'
response_server = requests.get(server_url, headers=HEADERS)
if response_server.status_code == 200:
    print(response_server.text[-2000:])
else:
    print(f"Failed to fetch server logs: {response_server.status_code} - {response_server.text}")
