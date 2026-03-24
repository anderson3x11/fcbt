import string
import secrets

def generate_password(length=24, uppercase=True, lowercase=True, digits=True, symbols=True):
    pool = ""
    if uppercase:
        pool += string.ascii_uppercase
    if lowercase:
        pool += string.ascii_lowercase
    if digits:
        pool += string.digits
    if symbols:
        pool += string.punctuation

    password = ""
    for i in range(length):
        password += secrets.choice(pool)
    
    return password