import json
import os
from dataclasses import asdict
from fcbt.crypto import encrypt, decrypt, derive_key
from fcbt.models import Vault, Entry

def save_vault(vault, password, file_name: str):
    salt = os.urandom(16)
    dico = asdict(vault)
    text = json.dumps(dico)
    salted_key = derive_key(password, salt)
    encrypted_text = encrypt(text, salted_key)
    
    with open(file_name, "wb") as f:
        f.write(salt + encrypted_text)

def load_vault(password, file_name: str):
    with open(file_name, "rb") as f:
        data = f.read()
    salt = data[:16]
    encrypted_text = data[16:]
    
    key = derive_key(password, salt)
    decrypted_text = decrypt(encrypted_text, key)
    
    dico = json.loads(decrypted_text)
    vault = Vault(entries=[Entry(**entry) for entry in dico["entries"]])
    return vault