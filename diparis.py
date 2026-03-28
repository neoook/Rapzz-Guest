import hmac
import hashlib
import requests
import string
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json
import time
from datetime import datetime
import urllib3
import os
import sys
from concurrent.futures import ThreadPoolExecutor
import base64
import threading

# Matikan warning insecure
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ================================
# CONFIGURATION
# ================================
TARGET_TOTAL = 1000
MAX_THREADS = 10
DEFAULT_REGION = "ID" 
NAME_PREFIX = "RAPZ"
PASS_PREFIX = "KEMONO"

SUCCESS_COUNTER = 0
ERROR_LOGS = []
LOCK = threading.Lock()

# Folder Structure
BASE_FOLDER = "AW"
TOKENS_FOLDER = os.path.join(BASE_FOLDER, "AW1")
ACCOUNTS_FOLDER = os.path.join(BASE_FOLDER, "AW2")

for folder in [BASE_FOLDER, TOKENS_FOLDER, ACCOUNTS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

REGION_LANG = {
    "ME": "ar", "IND": "hi", "ID": "id", "VN": "vi", "TH": "th", 
    "BD": "bn", "PK": "ur", "TW": "zh", "CIS": "ru", "SAC": "es", "BR": "pt"
}

HEX_KEY = "32656534343831396539623435393838343531343130363762323831363231383734643064356437616639643866376530306331653534373135623764316533"
KEY_HMAC = bytes.fromhex(HEX_KEY)

# ================================
# CRYPTO & PROTOCOL TOOLS
# ================================

def E_AEs(data_hex):
    k = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    v = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(k, AES.MODE_CBC, v)
    return cipher.encrypt(pad(bytes.fromhex(data_hex), 16))

def EnC_Vr(N):
    H = []
    while True:
        BesTo = N & 0x7F 
        N >>= 7
        if N: BesTo |= 0x80
        H.append(BesTo)
        if not N: break
    return bytes(H)

def CrEaTe_ProTo(fields):
    packet = bytearray()    
    for field, value in fields.items():
        if isinstance(value, int):
            packet.extend(EnC_Vr((field << 3) | 0) + EnC_Vr(value))
        elif isinstance(value, (str, bytes)):
            encoded = value.encode() if isinstance(value, str) else value
            packet.extend(EnC_Vr((field << 3) | 2) + EnC_Vr(len(encoded)) + encoded)
    return packet

def decode_id(jwt):
    try:
        payload = jwt.split('.')[1]
        payload += '=' * (4 - len(payload) % 4)
        data = json.loads(base64.urlsafe_b64decode(payload))
        return str(data.get('account_id') or data.get('external_id', 'N/A'))
    except: return "N/A"

# ================================
# WEB MONITORING LOGIC
# ================================

def update_status_json(current, total, last_id, error="None"):
    status_data = {
        "percent": round((current / total) * 100, 2),
        "current": current,
        "total": total,
        "last_id": last_id,
        "error": error,
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open("status.json", "w") as f:
        json.dump(status_data, f, indent=2)

# ================================
# MAIN ENGINE (OB52)
# ================================

def create_full_account():
    global ERROR_LOGS
    try:
        # 1. GUEST REGISTER
        pw = f"{PASS_PREFIX}_{''.join(random.choices(string.digits + string.ascii_letters, k=6))}"
        data = f"password={pw}&client_type=2&source=2&app_id=100067"
        sig = hmac.new(KEY_HMAC, data.encode(), hashlib.sha256).hexdigest()
        
        reg_guest = requests.post("https://100067.connect.garena.com/oauth/guest/register", 
                                 headers={"Authorization": f"Signature {sig}"}, data=data, timeout=10, verify=False).json()
        
        if 'uid' not in reg_guest: return None
        uid = reg_guest['uid']

        # 2. GRANT TOKEN
        token_res = requests.post("https://100067.connect.garena.com/oauth/guest/token/grant", 
                                 data={"uid": uid, "password": pw, "response_type": "token", "client_id": "100067", "client_secret": KEY_HMAC}, 
                                 timeout=10, verify=False).json()
        
        if 'access_token' not in token_res: return None
        acc_tok = token_res['access_token']
        open_id = token_res['open_id']

        # 3. MAJOR REGISTER
        name = f"{NAME_PREFIX}{random.randint(100,999)}⁰⁷"
        field_14 = "".join(chr(ord(open_id[i]) ^ [0x30, 0x30, 0x30, 0x32][i%4]) for i in range(len(open_id))).encode('latin1')
        
        reg_payload = CrEaTe_ProTo({1: name, 2: acc_tok, 3: open_id, 5: 102000007, 6: 4, 7: 1, 13: 1, 14: field_14, 15: REGION_LANG.get(DEFAULT_REGION, "en"), 16: 1, 17: 1})
        requests.post("https://loginbp.ggblueshark.com/MajorRegister", headers={"ReleaseVersion": "OB52"}, data=E_AEs(reg_payload.hex()), timeout=10, verify=False)

        # 4. MAJOR LOGIN
        login_hex = f"0a4d0a13323032352d30382d33302030353a31393a3231220966726565206669726528013a08312e3131342e31334232416e64726f6964204f532039202f204150492d3238202850492f72656c2e636a772e32303232303531382e313134313333294a0848616e6468656c64520a41544d204d6f62696c735a045749464960b60a68ee0572033330307a1f41524d7637205646507633204e454f4e20564d48207c2032343030207c20328001c90f8a010f416472656e6f2028544d29203634303932010d4f70656e474c20455320332e323961012b476f6f676c657c64666134616234622d396463342d343534652d383036352d6537306337333366613335666132010e3130352e3233352e3133392e393161610102{REGION_LANG.get(DEFAULT_REGION, 'en').hex()}b20120{open_id.hex()}ba010134c2010848616e6468656c64ca01104173757320415355535f4930303544416ea0140{acc_tok.hex()}f00101ca020a41544d204d6f62696c73d2020457494649"
        login_res = requests.post("https://loginbp.ggblueshark.com/MajorLogin", headers={"ReleaseVersion": "OB52"}, data=E_AEs(login_hex), timeout=10, verify=False)
        
        jwt = login_res.text[login_res.text.find("eyJ"):].split()[0][:150] if "eyJ" in login_res.text else ""
        
        return {
            "uid": uid, "password": pw, "name": name, 
            "account_id": decode_id(jwt), "region": DEFAULT_REGION,
            "status": "Success", "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        with LOCK: ERROR_LOGS.append(str(e))
        return None

def save_data(data):
    acc_file = os.path.join(ACCOUNTS_FOLDER, f"accounts-{DEFAULT_REGION}.json")
    current_list = []
    if os.path.exists(acc_file):
        try:
            with open(acc_file, 'r') as f: current_list = json.load(f)
        except: pass
    current_list.append(data)
    with open(acc_file, 'w') as f: json.dump(current_list, f, indent=2)

def worker():
    global SUCCESS_COUNTER
    while True:
        with LOCK:
            if SUCCESS_COUNTER >= TARGET_TOTAL: break
        
        acc = create_full_account()
        if acc:
            with LOCK:
                SUCCESS_COUNTER += 1
                save_data(acc)
                last_err = ERROR_LOGS[-1] if ERROR_LOGS else "None"
                update_status_json(SUCCESS_COUNTER, TARGET_TOTAL, acc['account_id'], last_err)
                percent = (SUCCESS_COUNTER / TARGET_TOTAL) * 100
                sys.stdout.write(f"\r🚀 [{SUCCESS_COUNTER}/{TARGET_TOTAL}] {percent:.1f}% | ID: {acc['account_id']} ")
                sys.stdout.flush()

if __name__ == "__main__":
    print(f"\n🔥 RAPZ AW ENGINE STARTING...")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for _ in range(MAX_THREADS):
            executor.submit(worker)
            
    print(f"\n✅ FINISHED! Time: {round(time.time() - start_time, 2)}s")
