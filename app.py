from flask import Flask, request, Response, send_from_directory, send_file
import json
import threading
import requests
from google.protobuf.json_format import MessageToJson
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
from collections import OrderedDict
import devxt_count_pb2
import dev_generator_pb2
from byte import Encrypt_ID, encrypt_api
import os
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__, static_folder='static')

def load_tokens(server="PK"):
    """Load tokens from server-specific JSON file"""
    try:
        filename = f"token_{server.lower()}.json"
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return None

def get_client_url(server):
    """Get client URL based on server region"""
    server = server.upper()
    
    # India region
    if server == "IND":
        return "https://client.ind.freefiremobile.com"
    
    # Americas region
    elif server in ["BR", "US", "SAC", "NA"]:
        return "https://client.us.freefiremobile.com"
    
    # Default: Asia/Europe/Middle East/Africa region
    # EU, ME, ID, TH, VN, SG, BD, PK, MY, PH, RU, AFR, Other
    else:
        return "https://clientbp.ggblueshark.com"

def encrypt_message(plaintext_bytes):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(plaintext_bytes, AES.block_size)
    encrypted = cipher.encrypt(padded)
    return binascii.hexlify(encrypted).decode('utf-8')

def create_uid_protobuf(uid):
    msg = dev_generator_pb2.dev_generator()
    msg.saturn_ = int(uid)
    msg.garena = 1
    return msg.SerializeToString()

def enc(uid):
    pb = create_uid_protobuf(uid)
    return encrypt_message(pb)

def decode_player_info(binary):
    info = devxt_count_pb2.xt()
    info.ParseFromString(binary)
    return info

def get_player_info(uid, server="PK"):
    tokens = load_tokens(server)
    if tokens is None:
        return None, None

    token = tokens[0]['token']
    base_url = get_client_url(server)
    url = f"{base_url}/GetPlayerPersonalShow"

    encrypted_uid = enc(uid)
    edata = bytes.fromhex(encrypted_uid)

    headers = {
        'User-Agent': "Dalvik/2.1.0",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/x-www-form-urlencoded",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB51"
    }

    response = requests.post(url, data=edata, headers=headers, verify=False, timeout=10)

    if response.status_code != 200:
        return None, None

    info = decode_player_info(response.content)
    data = json.loads(MessageToJson(info))

    account = data.get("AccountInfo", {})

    player_name = account.get("PlayerNickname", "Unknown")
    player_uid = account.get("UID", uid)

    return player_name, player_uid

def send_friend_request(uid, token, url, results, lock):
    try:
        encrypted_id = Encrypt_ID(uid)
        payload = f"08a7c4839f1e10{encrypted_id}1801"
        encrypted_payload = encrypt_api(payload)

        headers = {
            "Authorization": f"Bearer {token}",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB51",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0"
        }

        response = requests.post(url, data=bytes.fromhex(encrypted_payload), headers=headers, timeout=10)

        with lock:
            if response.status_code == 200:
                results['success'] += 1
            else:
                results['failed'] += 1

    except:
        with lock:
            results['failed'] += 1

@app.route("/", methods=["GET"])
def home():
    """Serve the main page"""
    return send_from_directory('static', 'index.html')

@app.route("/favicon.ico", methods=["GET"])
def favicon():
    """Serve the favicon"""
    favicon_path = os.path.join(os.path.dirname(__file__), 'static', 'favicon.png')
    if os.path.exists(favicon_path):
        return send_file(favicon_path, mimetype='image/png')
    else:
        # Return empty response if favicon doesn't exist
        return Response(status=204)

@app.route("/send_request-dev", methods=["GET"])
def handle_friend_request():
    uid = request.args.get("uid")
    server = request.args.get("server", "PK").upper()

    if not uid:
        return Response(json.dumps({"error": "uid required"}), mimetype="application/json")
    
    if not server:
        return Response(json.dumps({"error": "server required"}), mimetype="application/json")

    tokens = load_tokens(server)
    if tokens is None:
        return Response(json.dumps({"error": f"Token file not found for server: {server}"}), mimetype="application/json")

    player_name, player_uid = get_player_info(uid, server)

    base_url = get_client_url(server)
    url = f"{base_url}/RequestAddingFriend"

    results = {"success": 0, "failed": 0}
    lock = threading.Lock()
    threads = []

    for i in range(min(100, len(tokens))):
        token = tokens[i]['token']
        thread = threading.Thread(target=send_friend_request, args=(uid, token, url, results, lock))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    output = OrderedDict([
        ("PlayerName", player_name),
        ("UID", player_uid),
        ("Server", server),
        ("Success", results["success"]),
        ("Failed", results["failed"]),
        ("Status", 1 if results["success"] > 0 else 2)
    ])

    return Response(json.dumps(output), mimetype="application/json")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)