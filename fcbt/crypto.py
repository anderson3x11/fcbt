# import utility for Base64 encoding
import base64
# import Fernet
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def derive_key(master_password:str, salt:bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    # encode the derived key with Base64
    encoded_master_password = master_password.encode()
    key = base64.urlsafe_b64encode(kdf.derive(encoded_master_password))
    return key
    
def encrypt(data:str, key: bytes):
    fernet = Fernet(key)
    encoded_data = data.encode()
    return fernet.encrypt(encoded_data)
    
def decrypt(data: bytes, key: bytes):
    fernet = Fernet(key)
    return fernet.decrypt(data).decode()