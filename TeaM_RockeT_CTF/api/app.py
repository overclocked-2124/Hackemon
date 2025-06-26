from flask import Flask, render_template, request, jsonify, session
import secrets
import hashlib
import time
import base64
import json
import sqlite3
import struct
import os
from functools import wraps
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii

# Configure paths relative to the api directory for Vercel deployment
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')

app = Flask(__name__, 
           template_folder=template_folder,
           static_folder=static_folder)
app.secret_key = secrets.token_hex(32)

# For Vercel, we need to handle database path differently
# Use absolute path for database
db_base_path = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(db_base_path, '..', 'database')
os.makedirs(database_path, exist_ok=True)

class TeamRocketCrypto:
    def __init__(self):
        self.pokemon_types = {
            'Electric': 0x45, 'Ground': 0x47, 'Water': 0x57,
            'Grass': 0x4E, 'Fire': 0x46, 'Psychic': 0x50,
            'Dark': 0x44, 'Normal': 0x4E
        }
        
    def type_cipher(self, data, key_types):
        """Multi-layer encryption using Pokémon type effectiveness"""
        encrypted = bytearray()
        for i, byte in enumerate(data.encode() if isinstance(data, str) else data):
            type_key = self.pokemon_types[key_types[i % len(key_types)]]
            # Layer 1: XOR with type value
            temp = byte ^ type_key
            # Layer 2: Rotate bits based on type effectiveness
            temp = ((temp << 3) | (temp >> 5)) & 0xFF
            # Layer 3: Add Pokémon-themed constant
            temp = (temp + 0x96) & 0xFF  # 150 in hex (Mew)
            encrypted.append(temp)
        return bytes(encrypted)
    
    def reverse_type_cipher(self, data, key_types):
        """Reverse the Pokemon type cipher"""
        decrypted = bytearray()
        for i, byte in enumerate(data):
            type_key = self.pokemon_types[key_types[i % len(key_types)]]
            # Reverse Layer 3: Subtract Pokemon constant
            temp = (byte - 0x96) & 0xFF
            # Reverse Layer 2: Rotate bits back
            temp = ((temp >> 3) | (temp << 5)) & 0xFF
            # Reverse Layer 1: XOR with type value
            temp = temp ^ type_key
            decrypted.append(temp)
        return bytes(decrypted)
    
    def generate_challenge_data(self):
        """Generate encrypted challenge data"""
        flag = "CTF{TEAM_ROCKET_CRYPTO_MASTER_2025}"
        machine_types = ['Electric', 'Ground', 'Water', 'Grass', 'Fire']
        
        # Multi-stage encryption
        stage1 = self.type_cipher(flag, machine_types)
        stage2 = self._advanced_encrypt(stage1)
        
        return {
            'encrypted_flag': base64.b64encode(stage2).decode(),
            'machine_types': machine_types,
            'hint_data': self._generate_hints()
        }
    
    def _advanced_encrypt(self, data):
        """Advanced encryption layer"""
        key = b"GIOVANNI_MASTER_KEY_2025_SECRET!"[:32]  # 32 bytes for AES-256
        cipher = AES.new(key, AES.MODE_CBC)
        padded_data = pad(data, AES.block_size)
        return cipher.iv + cipher.encrypt(padded_data)
    
    def decrypt_flag(self, encrypted_b64, machine_types):
        """Complete decryption process"""
        try:
            # Step 1: Base64 decode
            ciphertext = base64.b64decode(encrypted_b64)
            
            # Step 2: AES decryption
            key = b"GIOVANNI_MASTER_KEY_2025_SECRET!"[:32]
            iv = ciphertext[:16]
            encrypted_data = ciphertext[16:]
            
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_padded = cipher.decrypt(encrypted_data)
            aes_decrypted = unpad(decrypted_padded, AES.block_size)
            
            # Step 3: Reverse type cipher
            final_decrypted = self.reverse_type_cipher(aes_decrypted, machine_types)
            
            # Step 4: Decode to text
            return final_decrypted.decode('utf-8')
        except Exception as e:
            return None
    
    def _generate_hints(self):
        """Generate progressive hints"""
        return [
            "Team Rocket uses Pokémon types as encryption keys...",
            "Look for patterns in the binary protocol messages",
            "The database has weak input validation - classic mistake!",
            "Type effectiveness values hide the decryption algorithm",
            "Chain multiple exploits: Protocol → Database → Crypto → Flag"
        ]

class RocketProtocol:
    def __init__(self):
        self.magic_bytes = b"\x52\x4F\x43\x4B"  # "ROCK"
        self.version = 0x01
        
    def encode_message(self, pokemon_id, command, payload):
        """Encode message in Team Rocket binary protocol"""
        header = struct.pack(">4sBHH", 
                           self.magic_bytes, 
                           self.version, 
                           pokemon_id, 
                           command)
        
        payload_bytes = payload.encode() if isinstance(payload, str) else payload
        length = len(payload_bytes)
        
        message = header + struct.pack(">H", length) + payload_bytes
        checksum = sum(message) & 0xFF
        
        return message + bytes([checksum])
    
    def decode_message(self, data):
        """Decode Team Rocket protocol message"""
        try:
            if len(data) < 10:
                return None
                
            magic, version, pokemon_id, command = struct.unpack(">4sBHH", data[:9])
            
            if magic != self.magic_bytes:
                return None
                
            length = struct.unpack(">H", data[9:11])[0]
            
            if len(data) < 11 + length + 1:
                return None
                
            payload = data[11:11+length]
            checksum = data[11+length]
            
            # Verify checksum
            calculated_checksum = sum(data[:-1]) & 0xFF
            if checksum != calculated_checksum:
                return None
                
            return {
                'pokemon_id': pokemon_id,
                'command': command,
                'payload': payload.decode('utf-8', errors='ignore'),
                'valid': True
            }
        except:
            return None

class VulnerableDatabase:
    def __init__(self):
        self.db_path = os.path.join(database_path, 'team_rocket.db')

    def search_pokemon(self, query, access_level=1):
        conn = sqlite3.connect(f'file:{self.db_path}?mode=ro', uri=True)
        cursor = conn.cursor()

        sql = f"SELECT * FROM pokemon_secrets WHERE name LIKE '%{query}%' AND access_level <= {access_level}"

        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            conn.close()
            return [("ERROR", str(e), "", "", "", 0, b"")]


    
    def search_pokemon(self, query, access_level=1):
        """Intentionally vulnerable search function"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # SQL Injection vulnerability - participants need to exploit this
        sql = f"SELECT * FROM pokemon_secrets WHERE name LIKE '%{query}%' AND access_level <= {access_level}"
        
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            conn.close()
            return [("ERROR", str(e), "", "", "", 0, b"")]

# Anti-cheat and session management
def rate_limit_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'last_request' not in session:
            session['last_request'] = 0
            session['request_count'] = 0
            
        current_time = time.time()
        
        # Rate limiting: 1 request per 100ms (reduced for testing)
        if current_time - session['last_request'] < 0.1:
            return jsonify({'error': 'Rate limit exceeded', 'retry_after': 0.1}), 429
            
        session['last_request'] = current_time
        session['request_count'] = session.get('request_count', 0) + 1
        
        # Prevent excessive requests
        if session['request_count'] > 500:
            return jsonify({'error': 'Too many requests', 'status': 'blocked'}), 403
            
        return f(*args, **kwargs)
    return decorated_function

# Initialize components
crypto = TeamRocketCrypto()
protocol = RocketProtocol()
database = VulnerableDatabase()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/challenge_data', methods=['POST'])
@rate_limit_check
def get_challenge_data():
    """Main challenge data endpoint"""
    challenge_data = crypto.generate_challenge_data()
    
    # Generate sample protocol messages
    sample_messages = []
    for i, ptype in enumerate(challenge_data['machine_types']):
        msg = protocol.encode_message(25 + i, 0x42 + i, f"TYPE_{ptype}_DATA")
        sample_messages.append({
            'hex': binascii.hexlify(msg).decode().upper(),
            'description': f"Intercepted {ptype} machine communication"
        })
    
    return jsonify({
        'encrypted_data': challenge_data['encrypted_flag'],
        'protocol_samples': sample_messages,
        'pokemon_types': list(crypto.pokemon_types.keys()),
        'database_hint': "Try searching for Pokémon in the database...",
        'story': {
            'title': "Operation: Crypto Rocket",
            'description': "You've infiltrated Team Rocket's secret facility. Multiple security layers protect their master plan.",
            'objectives': [
                "Analyze intercepted binary protocol messages",
                "Exploit the vulnerable Pokédex database",
                "Reverse engineer the custom encryption algorithm",
                "Chain exploits to recover the final flag"
            ]
        }
    })

@app.route('/api/protocol_analyze', methods=['POST'])
@rate_limit_check
def analyze_protocol():
    """Binary protocol analysis endpoint"""
    data = request.get_json()
    hex_input = data.get('hex_data', '').replace(' ', '').replace('\n', '')
    
    try:
        binary_data = binascii.unhexlify(hex_input)
        decoded = protocol.decode_message(binary_data)
        
        if decoded:
            return jsonify({
                'success': True,
                'decoded': decoded,
                'analysis': {
                    'magic_bytes': 'ROCK (Team Rocket signature)',
                    'pokemon_id': f"#{decoded.get('pokemon_id', 'Unknown')}",
                    'command': f"0x{decoded.get('command', 0):02X}",
                    'payload_length': len(decoded.get('payload', '')),
                    'payload': decoded.get('payload', '')
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid protocol format or corrupted data'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Hex decoding failed: {str(e)}'
        })

@app.route('/api/database_search', methods=['POST'])
@rate_limit_check
def search_database():
    """Vulnerable database search endpoint"""
    data = request.get_json()
    query = data.get('query', '')
    access_level = data.get('access_level', 1)
    
    # This is intentionally vulnerable to SQL injection
    results = database.search_pokemon(query, access_level)
    
    formatted_results = []
    for row in results:
        formatted_results.append({
            'id': row[0],
            'name': row[1],
            'type1': row[2],
            'type2': row[3],
            'secret_data': row[4],
            'access_level': row[5],
            'has_encrypted_payload': len(row[6]) > 0 if row[6] else False
        })
    
    return jsonify({
        'results': formatted_results,
        'count': len(formatted_results),
        'hint': "Higher access levels reveal more secrets..." if len(formatted_results) > 0 else "No results found"
    })

@app.route('/api/decrypt_challenge', methods=['POST'])
@rate_limit_check
def decrypt_challenge():
    """Final decryption challenge"""
    data = request.get_json()
    
    # Participants need to provide the correct decryption approach
    algorithm = data.get('algorithm', '')
    key_data = data.get('key_data', '')
    encrypted_input = data.get('encrypted_data', '')
    flag_attempt = data.get('flag', '')
    
    # Get the actual encrypted data from the challenge
    challenge_data = crypto.generate_challenge_data()
    actual_encrypted = challenge_data['encrypted_flag']
    
    # Validate the solution approach
    if (algorithm == 'team_rocket_multi_layer' and 
        'ROCKET_MASTER_KEY_DATA' in key_data):
        
        # Attempt decryption
        machine_types = ['Electric', 'Ground', 'Water', 'Grass', 'Fire']
        decrypted_flag = crypto.decrypt_flag(actual_encrypted, machine_types)
        
        if decrypted_flag and (decrypted_flag == flag_attempt or not flag_attempt):
            return jsonify({
                'success': True,
                'flag': decrypted_flag,
                'message': 'Congratulations! You successfully infiltrated Team Rocket\'s crypto system!'
            })
    
    return jsonify({
        'success': False,
        'message': 'Incorrect decryption approach. Ensure you have the right algorithm and master key!'
    })

@app.route('/api/hint', methods=['POST'])
@rate_limit_check
def get_hint():
    """Progressive hint system"""
    data = request.get_json()
    level = min(data.get('level', 1), 5)
    
    hints = crypto._generate_hints()
    
    return jsonify({
        'hint': hints[level - 1] if level <= len(hints) else "No more hints available!",
        'level': level,
        'max_level': len(hints)
    })

