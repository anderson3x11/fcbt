import json
from dataclasses import asdict
from fcbt.crypto import encrypt, decrypt
from fcbt.models import Vault, Entry

def save_vault(vault, key, file_name: str):
    dico = asdict(vault)
    text = json.dumps(dico)
    encrypted_text = encrypt(text, key)
    with open(file_name, "wb") as f:
        f.write(encrypted_text)

def load_vault(key, file_name: str):
    with open(file_name, "rb") as f:
        encrypted_text = f.read()
    decrypted_text = decrypt(encrypted_text, key)
    dico = json.loads(decrypted_text)
    vault = Vault(entries=[Entry(**entry) for entry in dico["entries"]])
    return vault