import hmac
import hashlib
import requests
import string
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json
import codecs
import time
from datetime import datetime
import urllib3
import os
import sys
import base64
import signal
import threading
import psutil
import re
import subprocess
import importlib

# Telegram Bot Imports
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Initialize
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ================================
# YOUR EXISTING SCRIPT FUNCTIONS
# ================================

def get_random_color():
    colors = ['\033[92m', '\033[93m', '\033[97m', '\033[94m']
    return random.choice(colors)

class Colors:
    BRIGHT = '\033[1m'
    RESET = '\033[0m'

EXIT_FLAG = False
SUCCESS_COUNTER = 0
TARGET_ACCOUNTS = 0
RARE_COUNTER = 0
COUPLES_COUNTER = 0
RARITY_SCORE_THRESHOLD = 3
LOCK = threading.Lock()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_FOLDER = os.path.join(CURRENT_DIR, "𝐁𝐑𝐄𝐗𝐗𝐄𝐑𝐀")
TOKENS_FOLDER = os.path.join(BASE_FOLDER, "𝐓𝐎𝐊𝐄𝐍𝐒𝐉𝐖𝐓")
ACCOUNTS_FOLDER = os.path.join(BASE_FOLDER, "𝐀𝐂𝐂𝐎𝐔𝐍𝐓𝐒")
RARE_ACCOUNTS_FOLDER = os.path.join(BASE_FOLDER, "𝐑𝐀𝐑𝐄𝐀𝐂𝐂𝐎𝐔𝐍𝐓𝐒")
COUPLES_ACCOUNTS_FOLDER = os.path.join(BASE_FOLDER, "𝐂𝐎𝐔𝐏𝐋𝐄𝐒𝐀𝐂𝐂𝐎𝐔𝐍𝐓𝐒")
GHOST_FOLDER = os.path.join(BASE_FOLDER, "𝐆𝐇𝐎𝐒𝐓")
GHOST_ACCOUNTS_FOLDER = os.path.join(GHOST_FOLDER, "𝐀𝐂𝐂𝐎𝐔𝐍𝐓𝐒")
GHOST_RARE_FOLDER = os.path.join(GHOST_FOLDER, "𝐑𝐀𝐑𝐄𝐀𝐂𝐂𝐎𝐔𝐍𝐓𝐒")
GHOST_COUPLES_FOLDER = os.path.join(GHOST_FOLDER, "𝐂𝐎𝐔𝐏𝐋𝐄𝐒𝐀𝐂𝐂𝐎𝐔𝐍𝐓𝐒")

for folder in [BASE_FOLDER, TOKENS_FOLDER, ACCOUNTS_FOLDER, RARE_ACCOUNTS_FOLDER, COUPLES_ACCOUNTS_FOLDER, GHOST_FOLDER, GHOST_ACCOUNTS_FOLDER, GHOST_RARE_FOLDER, GHOST_COUPLES_FOLDER]:
    os.makedirs(folder, exist_ok=True)

REGION_LANG = {"ME": "ar","IND": "hi","ID": "id","VN": "vi","TH": "th","BD": "bn","PK": "ur","TW": "zh","CIS": "ru","SAC": "es","BR": "pt"}
REGION_URLS = {"IND": "https://client.ind.freefiremobile.com/","ID": "https://clientbp.ggblueshark.com/","BR": "https://client.us.freefiremobile.com/","ME": "https://clientbp.common.ggbluefox.com/","VN": "https://clientbp.ggblueshark.com/","TH": "https://clientbp.common.ggbluefox.com/","CIS": "https://clientbp.ggblueshark.com/","BD": "https://clientbp.ggblueshark.com/","PK": "https://clientbp.ggblueshark.com/","SG": "https://clientbp.ggblueshark.com/","SAC": "https://client.us.freefiremobile.com/","TW": "https://clientbp.ggblueshark.com/"}
hex_key = "32656534343831396539623435393838343531343130363762323831363231383734643064356437616639643866376530306331653534373135623764316533"
key = bytes.fromhex(hex_key)
hex_data = "8J+agCBQUkVNSVVNIEFDQ09VTlQgR0VORVJBVE9SIPCfkqsgQnkgU1BJREVFUklPIHwgTm90IEZvciBTYWxlIPCfkas="
client_data = base64.b64decode(hex_data).decode('utf-8')
GARENA = "QllfU1BJREVFUklPX0dBTUlORw=="

FILE_LOCKS = {}

def get_file_lock(filename):
    if filename not in FILE_LOCKS:
        FILE_LOCKS[filename] = threading.Lock()
    return FILE_LOCKS[filename]

ACCOUNT_RARITY_PATTERNS = {
    "REPEATED_DIGITS_4": [r"(\d)\1{3,}", 3],
    "REPEATED_DIGITS_3": [r"(\d)\1\1(\d)\2\2", 2],
    "SEQUENTIAL_5": [r"(12345|23456|34567|45678|56789)", 4],
    "SEQUENTIAL_4": [r"(0123|1234|2345|3456|4567|5678|6789|9876|8765|7654|6543|5432|4321|3210)", 3],
    "PALINDROME_6": [r"^(\d)(\d)(\d)\3\2\1$", 5],
    "PALINDROME_4": [r"^(\d)(\d)\2\1$", 3],
    "SPECIAL_COMBINATIONS_HIGH": [r"(69|420|1337|007)", 4],
    "SPECIAL_COMBINATIONS_MED": [r"(100|200|300|400|500|666|777|888|999)", 2],
    "QUADRUPLE_DIGITS": [r"(1111|2222|3333|4444|5555|6666|7777|8888|9999|0000)", 4],
    "MIRROR_PATTERN_HIGH": [r"^(\d{2,3})\1$", 3],
    "MIRROR_PATTERN_MED": [r"(\d{2})0\1", 2],
    "GOLDEN_RATIO": [r"1618|0618", 3]
}

ACCOUNT_COUPLES_PATTERNS = {
    "MATCHING_PAIRS": [
        r"(\d{2})01.*\d{2}02",
        r"(\d{2})11.*\d{2}12",
        r"(\d{2})21.*\d{2}22",
    ],
    "COMPLEMENTARY_DIGITS": [
        r".*13.*14$",
        r".*07.*08$",
        r".*51.*52$",
    ],
    "LOVE_NUMBERS": [
        r".*520.*521$",
        r".*1314$",
    ]
}

POTENTIAL_COUPLES = {}
COUPLES_LOCK = threading.Lock()

def check_account_rarity(account_data):
    account_id = account_data.get("account_id", "")
    
    if account_id == "N/A" or not account_id:
        return False, None, None, 0
    
    rarity_score = 0
    detected_patterns = []
    
    for rarity_type, pattern_data in ACCOUNT_RARITY_PATTERNS.items():
        pattern = pattern_data[0]
        score = pattern_data[1]
        if re.search(pattern, account_id):
            rarity_score += score
            detected_patterns.append(rarity_type)
    
    account_id_digits = [int(d) for d in account_id if d.isdigit()]
    
    if len(set(account_id_digits)) == 1 and len(account_id_digits) >= 4:
        rarity_score += 5
        detected_patterns.append("UNIFORM_DIGITS")
    
    if len(account_id_digits) >= 4:
        differences = [account_id_digits[i+1] - account_id_digits[i] for i in range(len(account_id_digits)-1)]
        if len(set(differences)) == 1:
            rarity_score += 4
            detected_patterns.append("ARITHMETIC_SEQUENCE")
    
    if len(account_id) <= 8 and account_id.isdigit() and int(account_id) < 1000000:
        rarity_score += 3
        detected_patterns.append("LOW_ACCOUNT_ID")
    
    if rarity_score >= RARITY_SCORE_THRESHOLD:
        reason = f"Account ID {account_id} - Score: {rarity_score} - Patterns: {', '.join(detected_patterns)}"
        return True, "RARE_ACCOUNT", reason, rarity_score
    
    return False, None, None, rarity_score

def check_account_couples(account_data, thread_id):
    account_id = account_data.get("account_id", "")
    
    if account_id == "N/A" or not account_id:
        return False, None, None
    
    with COUPLES_LOCK:
        for stored_id, stored_data in POTENTIAL_COUPLES.items():
            stored_account_id = stored_data.get('account_id', '')
            
            couple_found, reason = check_account_couple_patterns(account_id, stored_account_id)
            if couple_found:
                partner_data = stored_data
                del POTENTIAL_COUPLES[stored_id]
                return True, reason, partner_data
        
        POTENTIAL_COUPLES[account_id] = {
            'uid': account_data.get('uid', ''),
            'account_id': account_id,
            'name': account_data.get('name', ''),
            'password': account_data.get('password', ''),
            'region': account_data.get('region', ''),
            'thread_id': thread_id,
            'timestamp': datetime.now().isoformat()
        }
    
    return False, None, None

def check_account_couple_patterns(account_id1, account_id2):
    if account_id1 and account_id2 and abs(int(account_id1) - int(account_id2)) == 1:
        return True, f"Sequential Account IDs: {account_id1} & {account_id2}"
    
    if account_id1 == account_id2[::-1]:
        return True, f"Mirror Account IDs: {account_id1} & {account_id2}"
    
    if account_id1 and account_id2:
        sum_acc = int(account_id1) + int(account_id2)
        if sum_acc % 1000 == 0 or sum_acc % 10000 == 0:
            return True, f"Complementary sum: {account_id1} + {account_id2} = {sum_acc}"
    
    love_numbers = ['520', '521', '1314', '3344']
    for love_num in love_numbers:
        if love_num in account_id1 and love_num in account_id2:
            return True, f"Both contain love number: {love_num}"
    
    return False, None

def save_rare_account(account_data, rarity_type, reason, rarity_score, is_ghost=False):
    try:
        if is_ghost:
            rare_filename = os.path.join(GHOST_RARE_FOLDER, "rare-ghost.json")
        else:
            region = account_data.get('region', 'UNKNOWN')
            rare_filename = os.path.join(RARE_ACCOUNTS_FOLDER, f"rare-{region}.json")
        
        rare_entry = {
            'uid': account_data["uid"],
            'password': account_data["password"],
            'account_id': account_data.get("account_id", "N/A"),
            'name': account_data["name"],
            'region': "𝐁𝐑𝐄𝐗𝐗" if is_ghost else account_data.get('region', 'UNKNOWN'),
            'rarity_type': rarity_type,
            'rarity_score': rarity_score,
            'reason': reason,
            'date_identified': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'jwt_token': account_data.get('jwt_token', ''),
            'thread_id': account_data.get('thread_id', 'N/A')
        }
        
        file_lock = get_file_lock(rare_filename)
        with file_lock:
            rare_list = []
            if os.path.exists(rare_filename):
                try:
                    with open(rare_filename, 'r', encoding='utf-8') as f:
                        rare_list = json.load(f)
                except (json.JSONDecodeError, IOError):
                    rare_list = []
            
            existing_ids = [acc.get('account_id') for acc in rare_list]
            if account_data.get("account_id", "N/A") not in existing_ids:
                rare_list.append(rare_entry)
                
                temp_filename = rare_filename + '.tmp'
                with open(temp_filename, 'w', encoding='utf-8') as f:
                    json.dump(rare_list, f, indent=2, ensure_ascii=False)
                os.replace(temp_filename, rare_filename)
                return True
            else:
                return False
        
    except Exception as e:
        print(f"❌ Error saving rare account: {e}")
        return False

def save_couples_account(account1, account2, reason, is_ghost=False):
    try:
        if is_ghost:
            couples_filename = os.path.join(GHOST_COUPLES_FOLDER, "couples-ghost.json")
        else:
            region = account1.get('region', 'UNKNOWN')
            couples_filename = os.path.join(COUPLES_ACCOUNTS_FOLDER, f"couples-{region}.json")
        
        couples_entry = {
            'couple_id': f"{account1.get('account_id', 'N/A')}_{account2.get('account_id', 'N/A')}",
            'account1': {
                'uid': account1["uid"],
                'password': account1["password"],
                'account_id': account1.get("account_id", "N/A"),
                'name': account1["name"],
                'thread_id': account1.get('thread_id', 'N/A')
            },
            'account2': {
                'uid': account2["uid"],
                'password': account2["password"],
                'account_id': account2.get("account_id", "N/A"),
                'name': account2["name"],
                'thread_id': account2.get('thread_id', 'N/A')
            },
            'reason': reason,
            'region': "𝐁𝐑𝐄𝐗𝐗" if is_ghost else account1.get('region', 'UNKNOWN'),
            'date_matched': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        file_lock = get_file_lock(couples_filename)
        with file_lock:
            couples_list = []
            if os.path.exists(couples_filename):
                try:
                    with open(couples_filename, 'r', encoding='utf-8') as f:
                        couples_list = json.load(f)
                except (json.JSONDecodeError, IOError):
                    couples_list = []
            
            existing_couples = [couple.get('couple_id') for couple in couples_list]
            if couples_entry['couple_id'] not in existing_couples:
                couples_list.append(couples_entry)
                
                temp_filename = couples_filename + '.tmp'
                with open(temp_filename, 'w', encoding='utf-8') as f:
                    json.dump(couples_list, f, indent=2, ensure_ascii=False)
                os.replace(temp_filename, couples_filename)
                return True
            else:
                return False
        
    except Exception as e:
        print(f"❌ Error saving couples account: {e}")
        return False

def generate_exponent_number():
    exponent_digits = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}
    number = random.randint(1, 99999)
    number_str = f"{number:05d}"
    exponent_str = ''.join(exponent_digits[digit] for digit in number_str)
    return exponent_str

def generate_random_name(base_name):
    exponent_part = generate_exponent_number()
    return f"{base_name[:7]}{exponent_part}"

def generate_custom_password(prefix):
    garena_decoded = base64.b64decode(GARENA).decode('utf-8')
    characters = string.ascii_uppercase + string.digits
    random_part1 = ''.join(random.choice(characters) for _ in range(5))
    random_part2 = ''.join(random.choice(characters) for _ in range(5))
    return f"{prefix}_Raozz_{random_part2}"

def EnC_Vr(N):
    if N < 0: 
        return b''
    H = []
    while True:
        BesTo = N & 0x7F 
        N >>= 7
        if N: 
            BesTo |= 0x80
        H.append(BesTo)
        if not N: 
            break
    return bytes(H)

def CrEaTe_VarianT(field_number, value):
    field_header = (field_number << 3) | 0
    return EnC_Vr(field_header) + EnC_Vr(value)

def CrEaTe_LenGTh(field_number, value):
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return EnC_Vr(field_header) + EnC_Vr(len(encoded_value)) + encoded_value

def CrEaTe_ProTo(fields):
    packet = bytearray()    
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = CrEaTe_ProTo(value)
            packet.extend(CrEaTe_LenGTh(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(CrEaTe_VarianT(field, value))           
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(CrEaTe_LenGTh(field, value))           
    return packet

def E_AEs(Pc):
    Z = bytes.fromhex(Pc)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    K = AES.new(key , AES.MODE_CBC , iv)
    R = K.encrypt(pad(Z , AES.block_size))
    return R

def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

def save_jwt_token(account_data, jwt_token, region, is_ghost=False):
    try:
        if is_ghost:
            token_filename = os.path.join(GHOST_FOLDER, "tokens-ghost.json")
        else:
            token_filename = os.path.join(TOKENS_FOLDER, f"tokens-{region}.json")
        
        token_entry = {
            'uid': account_data["uid"],
            'account_id': account_data.get("account_id", "N/A"),
            'jwt_token': jwt_token,
            'name': account_data["name"],
            'password': account_data["password"],
            'date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'region': "𝐁𝐑𝐄𝐗𝐗" if is_ghost else region,
            'thread_id': account_data.get('thread_id', 'N/A')
        }
        
        file_lock = get_file_lock(token_filename)
        with file_lock:
            tokens_list = []
            if os.path.exists(token_filename):
                try:
                    with open(token_filename, 'r', encoding='utf-8') as f:
                        tokens_list = json.load(f)
                except (json.JSONDecodeError, IOError):
                    tokens_list = []
            
            existing_account_ids = [token.get('account_id') for token in tokens_list]
            if account_data.get("account_id", "N/A") not in existing_account_ids:
                tokens_list.append(token_entry)
                
                temp_filename = token_filename + '.tmp'
                with open(temp_filename, 'w', encoding='utf-8') as f:
                    json.dump(tokens_list, f, indent=2, ensure_ascii=False)
                
                os.replace(temp_filename, token_filename)
                return True
            else:
                return False
        
    except Exception as e:
        print(f"❌ Error saving JWT token: {e}")
        return False

def save_normal_account(account_data, region, is_ghost=False):
    try:
        if is_ghost:
            account_filename = os.path.join(GHOST_ACCOUNTS_FOLDER, "ghost.json")
        else:
            account_filename = os.path.join(ACCOUNTS_FOLDER, f"accounts-{region}.json")
        
        account_entry = {
            'uid': account_data["uid"],
            'password': account_data["password"],
            'account_id': account_data.get("account_id", "N/A"),
            'name': account_data["name"],
            'region': "𝐁𝐑𝐄𝐗𝐗" if is_ghost else region,
            'date_created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'thread_id': account_data.get('thread_id', 'N/A')
        }
        
        file_lock = get_file_lock(account_filename)
        with file_lock:
            accounts_list = []
            if os.path.exists(account_filename):
                try:
                    with open(account_filename, 'r', encoding='utf-8') as f:
                        accounts_list = json.load(f)
                except (json.JSONDecodeError, IOError):
                    accounts_list = []
            
            existing_account_ids = [acc.get('account_id') for acc in accounts_list]
            if account_data.get("account_id", "N/A") not in existing_account_ids:
                accounts_list.append(account_entry)
                
                temp_filename = account_filename + '.tmp'
                with open(temp_filename, 'w', encoding='utf-8') as f:
                    json.dump(accounts_list, f, indent=2, ensure_ascii=False)
                
                os.replace(temp_filename, account_filename)
                return True
            else:
                return False
        
    except Exception as e:
        print(f"❌ Error saving normal account: {e}")
        return False

def smart_delay():
    time.sleep(random.uniform(1, 2))

def create_acc(region, account_name, password_prefix, is_ghost=False):
    if EXIT_FLAG:
        return None
    try:
        password = generate_custom_password(password_prefix)
        data = f"password={password}&client_type=2&source=2&app_id=100067"
        message = data.encode('utf-8')
        signature = hmac.new(key, message, hashlib.sha256).hexdigest()
        
        url = "https://100067.connect.garena.com/oauth/guest/register"
        headers = {
            "User-Agent": "GarenaMSDK/4.0.19P8(ASUS_Z01QD ;Android 12;en;US;)",
            "Authorization": "Signature " + signature,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }
        
        response = requests.post(url, headers=headers, data=data, timeout=30, verify=False)
        response.raise_for_status()
        
        if 'uid' in response.json():
            uid = response.json()['uid']
            print(f"✅ Guest account created: {uid}")
            smart_delay()
            return token(uid, password, region, account_name, password_prefix, is_ghost)
        return None
    except Exception as e:
        print(f"⚠️ Create account failed: {e}")
        smart_delay()
        return None

def token(uid, password, region, account_name, password_prefix, is_ghost=False):
    if EXIT_FLAG:
        return None
    try:
        url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        headers = {
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "100067.connect.garena.com",
            "User-Agent": "GarenaMSDK/4.0.19P8(ASUS_Z01QD ;Android 12;en;US;)",
        }
        body = {
            "uid": uid,
            "password": password,
            "response_type": "token",
            "client_type": "2",
            "client_secret": key,
            "client_id": "100067"
        }
        
        response = requests.post(url, headers=headers, data=body, timeout=30, verify=False)
        response.raise_for_status()
        
        if 'open_id' in response.json():
            open_id = response.json()['open_id']
            access_token = response.json()["access_token"]
            refresh_token = response.json()['refresh_token']
            
            result = encode_string(open_id)
            field = to_unicode_escaped(result['field_14'])
            field = codecs.decode(field, 'unicode_escape').encode('latin1')
            print(f"✅ Token granted for: {uid}")
            smart_delay()
            return Major_Regsiter(access_token, open_id, field, uid, password, region, account_name, password_prefix, is_ghost)
        return None
    except Exception as e:
        print(f"⚠️ Token grant failed: {e}")
        smart_delay()
        return None

def encode_string(original):
    keystream = [0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37,
                 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30]
    encoded = ""
    for i in range(len(original)):
        orig_byte = ord(original[i])
        key_byte = keystream[i % len(keystream)]
        result_byte = orig_byte ^ key_byte
        encoded += chr(result_byte)
    return {"open_id": original, "field_14": encoded}

def to_unicode_escaped(s):
    return ''.join(c if 32 <= ord(c) <= 126 else f'\\u{ord(c):04x}' for c in s)

def Major_Regsiter(access_token, open_id, field, uid, password, region, account_name, password_prefix, is_ghost=False):
    if EXIT_FLAG:
        return None
    try:
        if is_ghost:
            url = "https://loginbp.ggblueshark.com/MajorRegister"
        else:
            if region.upper() in ["ME", "TH"]:
                url = "https://loginbp.common.ggbluefox.com/MajorRegister"
            else:
                url = "https://loginbp.ggblueshark.com/MajorRegister"
            
        name = generate_random_name(account_name)
        
        headers = {
            "Accept-Encoding": "gzip",
            "Authorization": "Bearer",   
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue",
            "Host": "loginbp.ggblueshark.com" if is_ghost or region.upper() not in ["ME", "TH"] else "loginbp.common.ggbluefox.com",
            "ReleaseVersion": "OB52",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1",
            "X-Unity-Version": "2018.4."
        }

        lang_code = "pt" if is_ghost else REGION_LANG.get(region.upper(), "en")
        payload = {
            1: name,
            2: access_token,
            3: open_id,
            5: 102000007,
            6: 4,
            7: 1,
            13: 1,
            14: field,
            15: lang_code,
            16: 1,
            17: 1
        }

        payload_bytes = CrEaTe_ProTo(payload)
        encrypted_payload = E_AEs(payload_bytes.hex())
        
        response = requests.post(url, headers=headers, data=encrypted_payload, verify=False, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ MajorRegister successful: {name}")
            
            login_result = perform_major_login(uid, password, access_token, open_id, region, is_ghost)
            account_id = login_result.get("account_id", "N/A")
            jwt_token = login_result.get("jwt_token", "")
            
            if not is_ghost and jwt_token and account_id != "N/A" and region.upper() != "BR":
                region_bound = force_region_binding(region, jwt_token)
                if region_bound:
                    print(f"✅ Region {region} bound successfully!")
                else:
                    print(f"⚠️ Region binding failed for {region}")
            
            account_data = {
                "uid": uid, 
                "password": password, 
                "name": name, 
                "region": "GHOST" if is_ghost else region, 
                "status": "success",
                "account_id": account_id,
                "jwt_token": jwt_token
            }
            
            return account_data
        else:
            print(f"⚠️ MajorRegister returned status: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Major_Regsiter error: {str(e)}")
        smart_delay()
        return None

def perform_major_login(uid, password, access_token, open_id, region, is_ghost=False):
    try:
        lang = "pt" if is_ghost else REGION_LANG.get(region.upper(), "en")
        
        payload_parts = [
            b'\x1a\x132025-08-30 05:19:21"\tfree fire(\x01:\x081.114.13B2Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)J\x08HandheldR\nATM MobilsZ\x04WIFI`\xb6\nh\xee\x05r\x03300z\x1fARMv7 VFPv3 NEON VMH | 2400 | 2\x80\x01\xc9\x0f\x8a\x01\x0fAdreno (TM) 640\x92\x01\rOpenGL ES 3.2\x9a\x01+Google|dfa4ab4b-9dc4-454e-8065-e70c733fa53f\xa2\x01\x0e105.235.139.91\xaa\x01\x02',
            lang.encode("ascii"),
            b'\xb2\x01 1d8ec0240ede109973f3321b9354b44d\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x10Asus ASUS_I005DA\xea\x01@afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390\xf0\x01\x01\xca\x02\nATM Mobils\xd2\x02\x04WIFI\xca\x03 7428b253defc164018c604a1ebbfebdf\xe0\x03\xa8\x81\x02\xe8\x03\xf6\xe5\x01\xf0\x03\xaf\x13\xf8\x03\x84\x07\x80\x04\xe7\xf0\x01\x88\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02\xc8\x04\x01\xd2\x04=/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/lib/arm\xe0\x04\x01\xea\x04_2087f61c19f57f2af4e7feff0b24d9d9|/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/base.apk\xf0\x04\x03\xf8\x04\x01\x8a\x05\x0232\x9a\x05\n2019118692\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xe0\x05\xf3F\xea\x05\x07android\xf2\x05pKqsHT5ZLWrYljNb5Vqh//yFRlaPHSO9NWSQsVvOmdhEEn7W+VHNUK+Q+fduA3ptNrGB0Ll0LRz3WW0jOwesLj6aiU7sZ40p8BfUE/FI/jzSTwRe2\xf8\x05\xfb\xe4\x06\x88\x06\x01\x90\x06\x01\x9a\x06\x014\xa2\x06\x014\xb2\x06"GQ@O\x00\x0e^\x00D\x06UA\x0ePM\r\x13hZ\x07T\x06\x0cm\\V\x0ejYV;\x0bU5'
        ]
        
        payload = b''.join(payload_parts)
        
        if is_ghost:
            url = "https://loginbp.ggblueshark.com/MajorLogin"
        elif region.upper() in ["ME", "TH"]:
            url = "https://loginbp.common.ggbluefox.com/MajorLogin"
        else:
            url = "https://loginbp.ggblueshark.com/MajorLogin"
        
        headers = {
            "Accept-Encoding": "gzip",
            "Authorization": "Bearer",
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue",
            "Host": "loginbp.ggblueshark.com" if is_ghost or region.upper() not in ["ME", "TH"] else "loginbp.common.ggbluefox.com",
            "ReleaseVersion": "OB52",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1",
            "X-Unity-Version": "2018.4.11f1"
        }

        data = payload
        data = data.replace(b'afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390', access_token.encode())
        data = data.replace(b'1d8ec0240ede109973f3321b9354b44d', open_id.encode())
        
        d = encrypt_api(data.hex())
        final_payload = bytes.fromhex(d)

        response = requests.post(url, headers=headers, data=final_payload, verify=False, timeout=30)
        
        if response.status_code == 200 and len(response.text) > 10:
            jwt_start = response.text.find("eyJ")
            if jwt_start != -1:
                jwt_token = response.text[jwt_start:]
                second_dot = jwt_token.find(".", jwt_token.find(".") + 1)
                if second_dot != -1:
                    jwt_token = jwt_token[:second_dot + 44]
                    
                    account_id = decode_jwt_token(jwt_token)
                    return {"account_id": account_id, "jwt_token": jwt_token}
        
        return {"account_id": "N/A", "jwt_token": ""}
    except Exception as e:
        print(f"⚠️ MajorLogin failed: {e}")
        return {"account_id": "N/A", "jwt_token": ""}

def decode_jwt_token(jwt_token):
    try:
        parts = jwt_token.split('.')
        if len(parts) >= 2:
            payload_part = parts[1]
            padding = 4 - len(payload_part) % 4
            if padding != 4:
                payload_part += '=' * padding
            decoded = base64.urlsafe_b64decode(payload_part)
            data = json.loads(decoded)
            account_id = data.get('account_id') or data.get('external_id')
            if account_id:
                return str(account_id)
    except Exception as e:
        print(f"⚠️ JWT decode failed: {e}")
    return "N/A"

def force_region_binding(region, jwt_token):
    try:
        if region.upper() in ["ME", "TH"]:
            url = "https://loginbp.common.ggbluefox.com/ChooseRegion"
        else:
            url = "https://loginbp.ggblueshark.com/ChooseRegion"
        
        if region.upper() == "CIS":
            region_code = "RU"
        else:
            region_code = region.upper()
            
        fields = {1: region_code}
        proto_data = CrEaTe_ProTo(fields)
        encrypted_data = encrypt_api(proto_data.hex())
        payload = bytes.fromhex(encrypted_data)
        
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; M2101K7AG Build/SKQ1.210908.001)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/x-www-form-urlencoded",
            'Expect': "100-continue",
            'Authorization': f"Bearer {jwt_token}",
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': "OB52"
        }
        
        response = requests.post(url, data=payload, headers=headers, verify=False, timeout=30)
        return response.status_code == 200
    except Exception as e:
        print(f"⚠️ Region binding failed: {e}")
        return False

def generate_single_account(region, account_name, password_prefix, total_accounts, thread_id, is_ghost=False):
    global SUCCESS_COUNTER, RARE_COUNTER, COUPLES_COUNTER
    if EXIT_FLAG:
        return None
        
    with LOCK:
        if SUCCESS_COUNTER >= total_accounts:
            return None

    account_result = create_acc(region, account_name, password_prefix, is_ghost)
    if not account_result:
        return None

    account_id = account_result.get("account_id", "N/A")
    jwt_token = account_result.get("jwt_token", "")
    
    account_result['thread_id'] = thread_id

    with LOCK:
        SUCCESS_COUNTER += 1
        current_count = SUCCESS_COUNTER

    is_rare, rarity_type, rarity_reason, rarity_score = check_account_rarity(account_result)
    if is_rare:
        with LOCK:
            RARE_COUNTER += 1
        save_rare_account(account_result, rarity_type, rarity_reason, rarity_score, is_ghost)
    
    is_couple, couple_reason, partner_data = check_account_couples(account_result, thread_id)
    if is_couple and partner_data:
        with LOCK:
            COUPLES_COUNTER += 1
        save_couples_account(account_result, partner_data, couple_reason, is_ghost)
    
    if is_ghost:
        save_success = save_normal_account(account_result, "GHOST", is_ghost=True)
        if jwt_token:
            token_saved = save_jwt_token(account_result, jwt_token, "GHOST", is_ghost=True)
    else:
        save_success = save_normal_account(account_result, region)
        if jwt_token:
            token_saved = save_jwt_token(account_result, jwt_token, region)
    
    return {"account": account_result}

# ================================
# TELEGRAM  SECTION
# ================================

# Replace with your actual bot token from @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# User sessions management
user_sessions = {}

print("🤖 mizzu Telegram Bot Started...")

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    user_sessions[user_id] = {"step": "main"}
    
    welcome_text = """
🚀 **BISHAL Account Generator Bot** 🤖

✨ **Features:**
• 🌍 Multiple Region Support
• 👻 Ghost Mode Available  
• 💎 Rare Account Detection
• 💑 Couples Account Matching
• 📁 Automatic File Management

📋 **Available Commands:**
/generate - Create new accounts (Max 10000)
/stats - View statistics  
/download - Get account files
/help - Show help guide

Choose an option below:
    """
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        InlineKeyboardButton("🎯 Generate", callback_data="generate"),
        InlineKeyboardButton("📊 Stats", callback_data="stats"),
        InlineKeyboardButton("📁 Download", callback_data="download"),
        InlineKeyboardButton("ℹ️ Help", callback_data="help")
    ]
    
    keyboard.add(*buttons)
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "generate")
def generate_callback(call):
    show_region_selection(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "stats")  
def stats_callback(call):
    show_statistics(call)

@bot.callback_query_handler(func=lambda call: call.data == "download")
def download_callback(call):
    send_account_files(call)

@bot.callback_query_handler(func=lambda call: call.data == "help")
def help_callback(call):
    show_help(call)

@bot.callback_query_handler(func=lambda call: call.data == "back_main")
def back_main_callback(call):
    show_main_menu(call.message)

def show_main_menu(message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    buttons = [
        InlineKeyboardButton("🎯 Generate", callback_data="generate"),
        InlineKeyboardButton("📊 Stats", callback_data="stats"),
        InlineKeyboardButton("📁 Download", callback_data="download"),
        InlineKeyboardButton("ℹ️ Help", callback_data="help")
    ]
    
    keyboard.add(*buttons)
    
    bot.send_message(
        message.chat.id,
        "🤖 **Main Menu**\nChoose an option:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

def show_region_selection(message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    regions = [
        ("IND", "🇮🇳 India"),
        ("ID", "🇮🇩 Indonesia"), 
        ("VN", "🇻🇳 Vietnam"),
        ("TH", "🇹🇭 Thailand"),
        ("BD", "🇧🇩 Bangladesh"),
        ("PK", "🇵🇰 Pakistan"),
        ("ME", "🌍 Middle East"),
        ("GHOST", "👻 Ghost Mode")
    ]
    
    for region_code, region_name in regions:
        keyboard.add(InlineKeyboardButton(region_name, callback_data=f"region_{region_code}"))
    
    keyboard.add(InlineKeyboardButton("🔙 Back", callback_data="back_main"))
    
    bot.send_message(
        message.chat.id,
        "🌍 **Select Region:**\nChoose the region for account generation:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("region_"))
def region_selected(call):
    region = call.data.replace("region_", "")
    user_id = call.from_user.id
    
    user_sessions[user_id] = {
        "step": "waiting_count",
        "region": region
    }
    
    bot.edit_message_text(
        f"🌍 Selected: **{region}**\n\n"
        "📝 Now send me how many accounts to generate (1-10000):",
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: user_sessions.get(message.from_user.id, {}).get("step") == "waiting_count")
def handle_account_count(message):
    user_id = message.from_user.id
    session = user_sessions.get(user_id, {})
    
    try:
        count = int(message.text)
        if 1 <= count <= 10000:  # Changed from 20 to 30
            session["count"] = count
            session["step"] = "waiting_name"
            user_sessions[user_id] = session
            
            bot.send_message(
                message.chat.id,
                f"🎯 Count: **{count}** accounts\n\n"
                "👤 Now send the name prefix for accounts:",
                parse_mode="Markdown"
            )
        else:
            bot.send_message(message.chat.id, "❌ Please enter a number between 1-30")
            
    except ValueError:
        bot.send_message(message.chat.id, "❌ Please enter a valid number")

@bot.message_handler(func=lambda message: user_sessions.get(message.from_user.id, {}).get("step") == "waiting_name")
def handle_name_prefix(message):
    user_id = message.from_user.id
    session = user_sessions.get(user_id, {})
    
    if len(message.text) < 3:
        bot.send_message(message.chat.id, "❌ Name must be at least 3 characters")
        return
        
    session["name_prefix"] = message.text
    session["step"] = "waiting_password"
    user_sessions[user_id] = session
    
    bot.send_message(
        message.chat.id,
        f"👤 Name prefix: **{message.text}**\n\n"
        "🔑 Now send the password prefix:",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: user_sessions.get(message.from_user.id, {}).get("step") == "waiting_password")
def handle_password_prefix(message):
    user_id = message.from_user.id
    session = user_sessions.get(user_id, {})
    
    if len(message.text) < 3:
        bot.send_message(message.chat.id, "❌ Password prefix must be at least 3 characters")
        return
    
    # Show confirmation
    region_name = "👻 GHOST MODE" if session['region'] == "GHOST" else session['region']
    
    confirm_text = f"""
✅ **Generation Settings Confirmed:**

🌍 Region: **{region_name}**
🎯 Count: **{session['count']}** accounts  
👤 Name: **{session['name_prefix']}**
🔑 Password: **{message.text}**

⏳ Starting generation... This may take a few minutes.
    """
    
    progress_msg = bot.send_message(message.chat.id, confirm_text, parse_mode="Markdown")
    
    # Start generation in background thread
    thread = threading.Thread(
        target=generate_accounts_background,
        args=(user_id, session['region'], session['count'], session['name_prefix'], message.text, progress_msg.chat.id, progress_msg.message_id)
    )
    thread.daemon = True
    thread.start()
    
    # Reset session
    user_sessions[user_id] = {"step": "main"}

def generate_accounts_background(user_id, region, count, name_prefix, password_prefix, chat_id, progress_msg_id):
    global SUCCESS_COUNTER, RARE_COUNTER, COUPLES_COUNTER, TARGET_ACCOUNTS
    
    try:
        SUCCESS_COUNTER = 0
        TARGET_ACCOUNTS = count
        RARE_COUNTER = 0
        COUPLES_COUNTER = 0
        
        success_count = 0
        rare_count = 0
        couples_count = 0
        
        for i in range(count):
            if EXIT_FLAG:
                break
                
            result = generate_single_account(region, name_prefix, password_prefix, count, i+1, region=="GHOST")
            
            if result:
                success_count += 1
                
                # Check for rare accounts
                account_data = result.get("account", {})
                is_rare, _, _, _ = check_account_rarity(account_data)
                if is_rare:
                    rare_count += 1
                
                # Progress update every 3 accounts or when done
                if success_count % 3 == 0 or success_count == count:
                    progress_text = f"""
📊 **Generation Progress:**

✅ Generated: **{success_count}/{count}**
💎 Rare Found: **{rare_count}**
💑 Couples: **{couples_count}**

⏳ Continuing...
                    """
                    try:
                        bot.edit_message_text(
                            progress_text,
                            chat_id,
                            progress_msg_id,
                            parse_mode="Markdown"
                        )
                    except:
                        pass
        
        # Final report
        final_text = f"""
🎉 **Generation Complete!**

📊 **Results:**
✅ Success: **{success_count}/{count}**
💎 Rare Accounts: **{rare_count}** 
💑 Couples Pairs: **{couples_count}**
🌍 Region: **{region}**

📁 Accounts saved successfully!
Use 📁 Download button to get account files.
        """
        
        bot.edit_message_text(
            final_text,
            chat_id,
            progress_msg_id,
            parse_mode="Markdown"
        )
        
    except Exception as e:
        error_msg = f"❌ Generation failed: {str(e)}"
        try:
            bot.edit_message_text(
                error_msg,
                chat_id,
                progress_msg_id
            )
        except:
            bot.send_message(chat_id, error_msg)

def show_statistics(call):
    try:
        total_accounts = 0
        regional_stats = []
        
        # Count regular accounts
        if os.path.exists(ACCOUNTS_FOLDER):
            for file in os.listdir(ACCOUNTS_FOLDER):
                if file.endswith('.json'):
                    file_path = os.path.join(ACCOUNTS_FOLDER, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            accounts = json.load(f)
                            count = len(accounts)
                            total_accounts += count
                            region_name = file.replace('accounts-', '').replace('.json', '')
                            regional_stats.append(f"• {region_name}: {count}")
                    except:
                        pass
        
        # Count ghost accounts
        ghost_file = os.path.join(GHOST_ACCOUNTS_FOLDER, "ghost.json")
        if os.path.exists(ghost_file):
            try:
                with open(ghost_file, 'r', encoding='utf-8') as f:
                    ghost_accounts = json.load(f)
                    ghost_count = len(ghost_accounts)
                    total_accounts += ghost_count
                    regional_stats.append(f"• GHOST: {ghost_count}")
            except:
                pass
        
        stats_text = f"""
📊 **Bot Statistics**

📁 Total Accounts: **{total_accounts}**
🌍 Available Regions: **{len(REGION_LANG)}**
💎 Rarity System: **Active**
💑 Couples Detection: **Enabled**

**Regional Breakdown:**
{chr(10).join(regional_stats) if regional_stats else "• No accounts yet"}
        """
        
        bot.edit_message_text(
            stats_text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown"
        )
        
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ Error loading statistics: {str(e)}")

def send_account_files(call):
    try:
        bot.send_message(call.message.chat.id, "📁 Preparing account files...")
        
        account_files = []
        
        # Regular accounts
        if os.path.exists(ACCOUNTS_FOLDER):
            for file in os.listdir(ACCOUNTS_FOLDER):
                if file.endswith('.json'):
                    file_path = os.path.join(ACCOUNTS_FOLDER, file)
                    if os.path.getsize(file_path) > 0:
                        account_files.append(file_path)
        
        # Ghost accounts
        ghost_file = os.path.join(GHOST_ACCOUNTS_FOLDER, "ghost.json")
        if os.path.exists(ghost_file) and os.path.getsize(ghost_file) > 0:
            account_files.append(ghost_file)
        
        if account_files:
            for file_path in account_files[:5]:  # Increased to 5 files
                try:
                    with open(file_path, 'rb') as f:
                        bot.send_document(
                            call.message.chat.id,
                            f,
                            caption=f"📁 {os.path.basename(file_path)}"
                        )
                    time.sleep(1)  # Avoid rate limiting
                except Exception as e:
                    bot.send_message(call.message.chat.id, f"❌ Error sending {os.path.basename(file_path)}: {str(e)}")
            
            if len(account_files) > 5:
                bot.send_message(call.message.chat.id, f"📝 Showing 5 of {len(account_files)} files. More files available in the storage folder.")
        else:
            bot.send_message(call.message.chat.id, "📭 No account files found. Generate some accounts first!")
            
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ Error: {str(e)}")

def show_help(call):
    help_text = """
🤖 **BISHAL Account Generator Bot - Help**

**📋 Available Commands:**
/start - Start the bot
/generate - Create new accounts (Max0)  
/stats - View statistics
/download - Get account files

**🌍 Supported Regions:**
IND, ID, VN, TH, BD, PK, ME, GHOST

**✨ Features:**
• Multi-region account generation
• Ghost mode for special accounts  
• Rare account detection system
• Couples account matching
• Automatic file management
• Real-time progress updates

**⚡ Usage Guide:**
1. Click 🎯 Generate
2. Select region
3. Enter account count (1-30)
4. Provide name prefix  
5. Provide password prefix
6. Wait for generation
7. Download files when done

**📝 Notes:**
• Maximum 30 accounts per batch
• Files are saved automatically
• Use download to get JSON files
• Bot works 24/7
    """
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🚀 Start Generating", callback_data="generate"))
    
    bot.edit_message_text(
        help_text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['generate'])
def generate_command(message):
    show_region_selection(message)

@bot.message_handler(commands=['stats'])  
def stats_command(message):
    msg = type('Message', (), {'chat': type('Chat', (), {'id': message.chat.id})(), 'message_id': message.message_id})()
    call = type('Call', (), {'message': msg})()
    show_statistics(call)

@bot.message_handler(commands=['download'])
def download_command(message):
    msg = type('Message', (), {'chat': type('Chat', (), {'id': message.chat.id})(), 'message_id': message.message_id})()
    call = type('Call', (), {'message': msg})()
    send_account_files(call)

@bot.message_handler(commands=['help'])
def help_command(message):
    msg = type('Message', (), {'chat': type('Chat', (), {'id': message.chat.id})(), 'message_id': message.message_id})()
    call = type('Call', (), {'message': msg})()
    show_help(call)

# Error handler
@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    user_id = message.from_user.id
    current_step = user_sessions.get(user_id, {}).get("step", "main")
    
    if current_step == "main":
        bot.send_message(
            message.chat.id,
            "🤖 Use the menu buttons or commands:\n"
            "/generate - Create accounts (Max 30)\n"  
            "/stats - View statistics\n"
            "/download - Get files\n"
            "/help - Show help"
        )

def install_requirements():
    required_packages = [
        'requests',
        'pycryptodome',
        'telebot',
        'urllib3',
        'psutil'
    ]
    
    print("🔍 Checking required packages...")
    
    for package in required_packages:
        try:
            if package == 'pycryptodome':
                import Crypto
            elif package == 'telebot':
                import telebot
            else:
                importlib.import_module(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"⚠️ Installing {package}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ {package} installed successfully")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                return False
    return True

if __name__ == "__main__":
    print("🚀 Starting BISHAL Telegram Bot...")
    
    if install_requirements():
        print("🤖 Bot is running...")
        print("📝 Make sure to replace 'YOUR_BOT_TOKEN_HERE' with your actual bot token!")
        
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"❌ Bot error: {e}")
            print("🔄 Restarting in 5 seconds...")
            time.sleep(5)
            os.execv(sys.executable, [sys.executable] + sys.argv)
