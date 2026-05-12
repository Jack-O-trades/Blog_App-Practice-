import os
import zipfile
import requests
import time
import sys

USERNAME = 'OmmPrakashRout'
TOKEN = '1b91f1de98051abd74ec1166f099d0d979e1dab6'
DOMAIN = f'{USERNAME}.pythonanywhere.com'
API_BASE = f'https://www.pythonanywhere.com/api/v0/user/{USERNAME}/'
HEADERS = {'Authorization': f'Token {TOKEN}'}

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_NAME = os.path.basename(PROJECT_DIR)
ZIP_FILE = f'{PROJECT_NAME}.zip'

def create_zip():
    print("Creating zip file...")
    with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_DIR):
            if 'venv' in root or '__pycache__' in root or '.git' in root:
                continue
            for file in files:
                if file.endswith('.zip') or file == 'db.sqlite3' or file == '.DS_Store' or file == 'deploy_to_pa.py' or file == 'quick_reload.py':
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, PROJECT_DIR)
                zipf.write(file_path, arcname)
    print("Zip file created.")

def upload_zip():
    print("Uploading zip file...")
    url = f"{API_BASE}files/path/home/{USERNAME}/{ZIP_FILE}"
    with open(ZIP_FILE, 'rb') as f:
        response = requests.post(url, headers=HEADERS, files={'content': f})
    if response.status_code in [200, 201]:
        print("Upload successful.")
    else:
        print(f"Failed to upload: {response.text}")
        sys.exit(1)

def run_extraction_and_install():
    print("Extracting and installing via console...")
    helper_code = f"""
import zipfile
import os
import subprocess

try:
    with zipfile.ZipFile('/home/{USERNAME}/{ZIP_FILE}', 'r') as zip_ref:
        zip_ref.extractall('/home/{USERNAME}/{PROJECT_NAME}')
    subprocess.check_call(['pip3.10', 'install', 'django', '--user'])
    subprocess.check_call(['python3.10', '/home/{USERNAME}/{PROJECT_NAME}/manage.py', 'migrate'])
    print('SUCCESS_DEPLOYMENT')
except Exception as e:
    print('ERROR_DEPLOYMENT:', e)
"""
    requests.post(f"{API_BASE}files/path/home/{USERNAME}/deploy_helper.py", headers=HEADERS, files={'content': helper_code})
    
    r = requests.post(f"{API_BASE}consoles/", headers=HEADERS, data={'executable': 'python3.10'})
    c_id = r.json()['id']
    print("Waiting for console to start...")
    time.sleep(15)
    
    requests.post(f"{API_BASE}consoles/{c_id}/send_input/", headers=HEADERS, data={'input': 'import deploy_helper\\n'})
    
    print("Waiting for extraction and installation to finish... (this can take 1-2 minutes)")
    for _ in range(20):
        time.sleep(10)
        out = requests.get(f"{API_BASE}consoles/{c_id}/get_latest_output/", headers=HEADERS).json()
        text = out.get('output', '')
        if 'SUCCESS_DEPLOYMENT' in text or 'ERROR_DEPLOYMENT' in text:
            print("Console output:")
            print(text)
            break
            
    requests.delete(f"{API_BASE}consoles/{c_id}/", headers=HEADERS)

def setup_webapp():
    print("Setting up webapp...")
    response = requests.get(f"{API_BASE}webapps/{DOMAIN}/", headers=HEADERS)
    if response.status_code == 404:
        print("Creating new webapp...")
        data = {
            'domain_name': DOMAIN,
            'python_version': 'python310',
        }
        resp = requests.post(f"{API_BASE}webapps/", headers=HEADERS, data=data)
        if resp.status_code != 201:
            print(f"Failed to create webapp: {resp.text}")
            sys.exit(1)
    else:
        print("Webapp already exists.")

def configure_wsgi():
    print("Configuring WSGI file...")
    wsgi_path = f"/var/www/{DOMAIN.lower().replace('.', '_')}_wsgi.py"
    wsgi_content = f"""
import os
import sys

path = '/home/{USERNAME}/{PROJECT_NAME}'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = '{PROJECT_NAME}.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
"""
    url = f"{API_BASE}files/path{wsgi_path}"
    response = requests.post(url, headers=HEADERS, files={'content': wsgi_content})
    if response.status_code not in [200, 201]:
        print(f"Failed to update WSGI: {response.text}")

def reload_webapp():
    print("Reloading webapp...")
    response = requests.post(f"{API_BASE}webapps/{DOMAIN}/reload/", headers=HEADERS)
    if response.status_code == 200:
        print("Webapp reloaded successfully!")
    else:
        print(f"Failed to reload webapp: {response.text}")

if __name__ == "__main__":
    try:
        create_zip()
        upload_zip()
        run_extraction_and_install()
        setup_webapp()
        configure_wsgi()
        reload_webapp()
        print(f"\\nDeployment complete! Visit http://{DOMAIN}")
    except requests.exceptions.ConnectionError:
        print("Network error connecting to PythonAnywhere. Please try again later.")
