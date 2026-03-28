import telebot
from telebot import types
import requests
import threading
import time
import random
import string
import json
import hmac
import hashlib
import base64
import os
import codecs
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ==========================================
# 🛑 WARNINGS OFF & CONFIGURATION
# ==========================================
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 👇 YAHAN APNA BOT TOKEN DAALO 👇
API_TOKEN = os.getenv('BOT_TOKEN') 

bot = telebot.TeleBot(API_TOKEN)

# Proxy Configuration (Tor Must Run on 9050)
PROXIES = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

user_data = {}

# ==========================================
# 🔐 CRYPTO & UTILS (CORE LOGIC)
# ==========================================

def EnC_Vr(N):
    if N < 0: return b''
    H = []
    while True:
        BesTo = N & 0x7F 
        N >>= 7
        if N: BesTo |= 0x80
        H.append(BesTo)
        if not N: break
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
    return K.encrypt(pad(Z , AES.block_size))

def generate_exponent_number():
    exponent_digits = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}
    number = random.randint(1, 99999)
    number_str = f"{number:05d}"
    return ''.join(exponent_digits[digit] for digit in number_str)

def generate_random_name(base_name):
    return f"{base_name[:7]}{generate_exponent_number()}"

def generate_custom_password(prefix):
    characters = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choice(characters) for _ in range(5))
    return f"{prefix}_LewRao_{random_part}"

def encode_string(original):
    keystream = [0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30]
    encoded = ""
    for i in range(len(original)):
        orig_byte = ord(original[i])
        key_byte = keystream[i % len(keystream)]
        result_byte = orig_byte ^ key_byte
        encoded += chr(result_byte)
    return {"open_id": original, "field_14": encoded}

def to_unicode_escaped(s):
    result = []
    for c in s:
        if 32 <= ord(c) <= 126: result.append(c)
        else: result.append(r'\u{:04x}'.format(ord(c)))
    return ''.join(result)

# API POOL
MAIN_HEX_KEY = "32656534343831396539623435393838343531343130363762323831363231383734643064356437616639643866376530306331653534373135623764316533"
API_POOL = [{"id": "100067", "key": bytes.fromhex(MAIN_HEX_KEY), "label": f"API {i:02d}"} for i in range(1, 8)]

# ==========================================
# 🚀 FAST GARENA LOGIC
# ==========================================

def get_session():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry, pool_connections=50, pool_maxsize=50)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.proxies.update(PROXIES)
    session.verify = False
    return session

def logic_create_acc(region, account_name, password_prefix, session):
    try:
        current_api = random.choice(API_POOL)
        app_id = current_api["id"]
        secret_key = current_api["key"]
        password = generate_custom_password(password_prefix)
        data = f"password={password}&client_type=2&source=2&app_id={app_id}"
        message = data.encode('utf-8')
        signature = hmac.new(secret_key, message, hashlib.sha256).hexdigest()
        
        headers = {
            "User-Agent": "GarenaMSDK/4.0.19P8(ASUS_Z01QD ;Android 12;en;US;)",
            "Authorization": "Signature " + signature,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        url = f"https://{app_id}.connect.garena.com/oauth/guest/register"
        resp = session.post(url, headers=headers, data=data, timeout=10)
        
        if 'uid' in resp.json():
            uid = resp.json()['uid']
            return logic_token(uid, password, region, account_name, password_prefix, current_api, session)
        return None
    except:
        return None

def logic_token(uid, password, region, account_name, password_prefix, api_config, session):
    try:
        app_id = api_config["id"]
        secret_key = api_config["key"]
        url = f"https://{app_id}.connect.garena.com/oauth/guest/token/grant"
        body = {
            "uid": uid, "password": password, "response_type": "token",
            "client_type": "2", "client_secret": secret_key, "client_id": app_id
        }
        resp = session.post(url, data=body, timeout=10)
        if 'access_token' in resp.json():
            data = resp.json()
            enc = encode_string(data['open_id'])
            field = to_unicode_escaped(enc['field_14'])
            field = codecs.decode(field, 'unicode_escape').encode('latin1')
            
            return logic_major_register(data['access_token'], data['open_id'], field, uid, password, region, account_name, session)
        return None
    except:
        return None

def logic_major_register(access_token, open_id, field, uid, password, region, account_name, session):
    try:
        url = "https://loginbp.ggblueshark.com/MajorRegister"
        name = generate_random_name(account_name)
        headers = {
            "ReleaseVersion": "OB52",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1"
        }
        
        payload = {1: name, 2: access_token, 3: open_id, 5: 102000007, 6: 4, 7: 1, 13: 1, 14: field, 15: "en", 16: 1, 17: 1}
        payload_bytes = CrEaTe_ProTo(payload)
        encrypted = E_AEs(payload_bytes.hex())
        
        resp = session.post(url, headers=headers, data=encrypted, timeout=10)
        if resp.status_code == 200:
            return {"uid": uid, "password": password, "name": name, "region": region}
        return None
    except:
        return None

# ==========================================
# 🤖 BOT INTERFACE
# ==========================================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🚀 START GENERATION", callback_data='start_gen')
    btn2 = types.InlineKeyboardButton("ℹ️ HELP", callback_data='help')
    markup.add(btn1, btn2)
    
    welcome = (
        f"🔥 **SR KING ULTIMATE BOT** 🔥\n\n"
        f"👋 Welcome {message.from_user.first_name}!\n"
        f"⚡ Status: **ONLINE**\n"
        f"🛡️ Protection: **TOR + WARP**\n\n"
        f"👇 Click button to generate accounts:"
    )
    bot.send_message(message.chat.id, welcome, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    
    if call.data == 'start_gen':
        bot.answer_callback_query(call.id)
        msg = bot.send_message(chat_id, "🔢 **Kitne Accounts Banane Hain?**\n(Number likho, e.g. 50)", parse_mode='Markdown')
        bot.register_next_step_handler(msg, step_count)
        
    elif call.data == 'help':
        bot.answer_callback_query(call.id, text="Commands use karo bhai!", show_alert=True)

    elif call.data.startswith('reg_'):
        # Fix: Immediately answer query to stop spinning
        bot.answer_callback_query(call.id, text="🚀 Starting Process...")
        
        try:
            region = call.data.split('_')[1]
            if chat_id not in user_data:
                bot.send_message(chat_id, "⚠️ **Session Expired!** Type /start again.")
                return

            count = user_data[chat_id]['count']
            name = user_data[chat_id]['name']
            pasw = user_data[chat_id]['pass']
            
            status_msg = bot.send_message(
                chat_id,
                f"⚡ **TASK STARTED**\n\n🌍 Region: `{region}`\n🎯 Target: `{count}`\n⏳ Initializing Engines...",
                parse_mode='Markdown'
            )
            
            # Start Background Thread
            threading.Thread(target=worker_process, args=(chat_id, count, name, pasw, region, status_msg.message_id)).start()
            
        except Exception as e:
            bot.send_message(chat_id, f"❌ Error: {str(e)}")

# ==========================================
# 👣 INPUT STEPS
# ==========================================

def step_count(message):
    try:
        count = int(message.text)
        user_data[message.chat.id] = {'count': count}
        msg = bot.send_message(message.chat.id, "👤 **Name Prefix Kya Hoga?**\n(e.g. SRK)", parse_mode='Markdown')
        bot.register_next_step_handler(msg, step_name)
    except:
        bot.send_message(message.chat.id, "❌ Number only!")

def step_name(message):
    user_data[message.chat.id]['name'] = message.text
    msg = bot.send_message(message.chat.id, "🔑 **Password Prefix Kya Hoga?**\n(e.g. PASS)", parse_mode='Markdown')
    bot.register_next_step_handler(msg, step_pass)

def step_pass(message):
    user_data[message.chat.id]['pass'] = message.text
    
    markup = types.InlineKeyboardMarkup(row_width=3)
    regions = ["IND", "BD", "SG", "EU", "RU", "BR"]
    btns = [types.InlineKeyboardButton(r, callback_data=f'reg_{r}') for r in regions]
    markup.add(*btns)
    
    bot.send_message(message.chat.id, "🌍 **Region Select Karo:**", reply_markup=markup)

# ==========================================
# 🛠️ WORKER ENGINE
# ==========================================

def worker_process(chat_id, total, name_prefix, pass_prefix, region, message_id):
    try:
        session = get_session()
        
        # Test Tor Connection (Silently)
        try:
            session.get("https://check.torproject.org", timeout=5)
        except:
            bot.edit_message_text(chat_id, message_id, "❌ **TOR ERROR**\nTermux me `tor` command chalao!")
            return

        success = 0
        results = []
        start_time = time.time()
        
        # Speed Loop
        for i in range(1, total + 1):
            acc = logic_create_acc(region, name_prefix, pass_prefix, session)
            
            if acc:
                success += 1
                results.append(f"UID: {acc['uid']} | PASS: {acc['password']} | NAME: {acc['name']}")
            
            # Smart Update (Avoids flood limit)
            if i % 5 == 0 or i == total:
                percent = (i / total) * 100
                bar = '█' * int(percent / 10) + '░' * (10 - int(percent / 10))
                elapsed = int(time.time() - start_time)
                speed = round(i / elapsed, 2) if elapsed > 0 else 0
                
                msg = (
                    f"⚡ **SR KING GENERATING...**\n\n"
                    f"📊 Progress: `{bar}` {int(percent)}%\n"
                    f"✅ Success: `{success}`\n"
                    f"🚀 Speed: `{speed} acc/s`\n"
                    f"⏱️ Time: `{elapsed}s`"
                )
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=msg, parse_mode='Markdown')
                except:
                    pass
            
            # Fast Sleep (0.2s is fast but safe enough)
            time.sleep(0.2)
            
        # Create and Send File
        if results:
            filename = f"SRKING_{region}_{random.randint(1000,9999)}.txt"
            with open(filename, "w") as f:
                f.write(f"SR KING ULTIMATE - REGION: {region}\n")
                f.write("=====================================\n")
                for line in results:
                    f.write(line + "\n")
            
            with open(filename, "rb") as f:
                bot.send_document(
                    chat_id, 
                    f, 
                    caption=f"✅ **COMPLETED!**\n\n📂 Total Generated: {success}\n⚡ Speed: High\n👤 Dev: @SRking5306"
                )
            os.remove(filename)
        else:
            bot.edit_message_text(chat_id, message_id, "❌ **Failed!**\nEk bhi account nahi bana. Shayad Proxy/IP ban hai.")
            
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Fatal Error: {str(e)}")

# ==========================================
# ▶️ RUNNER
# ==========================================
if __name__ == "__main__":
    print("🤖 SR KING BOT STARTING...")
    print("✅ Waiting for Tor...")
    try:
        # Initial check
        s = requests.Session()
        s.proxies = PROXIES
        s.verify = False
        r = s.get('https://check.torproject.org/api/ip', timeout=10)
        print(f"✅ CONNECTED! IP: {r.json().get('IP', 'Unknown')}")
        print("🚀 BOT IS LIVE! GO TO TELEGRAM.")
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print("\n❌ ERROR: Tor nahi chal raha!")
        print("👉 Termux me type karo: tor")
        print(f"Details: {e}")
