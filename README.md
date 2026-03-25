# FCBT - First City Bank and Trust

A local password manager built in Python. Your vault is encrypted with AES (Fernet) using a master password, and stored locally on your machine.

## Features

- Encrypted vault (AES via Fernet + PBKDF2 key derivation with random salt)
- Add, search, modify and delete entries
- Automatic password generation
- Change master password
- Data never leaves your machine

## Installation

```bash
git clone https://github.com/anderson3x11/fcbt.git
cd fcbt
python -m venv .venv
.venv\Scripts\activate # or source .venv/bin/activate on Linux
pip install cryptography
```

## Usage

```bash
python -m fcbt.cli
```

You will be prompted to enter a password
On first launch, a new vault is created with that password. On subsequent launches, your existing vault is loaded.

## Project structure

```
fcbt/
  __init__.py
  models.py      # Entry and Vault dataclasses
  generator.py   # Secure password generation (secrets module)
  crypto.py      # Key derivation (PBKDF2) + encrypt/decrypt (Fernet)
  storage.py     # Save/load vault (salt + encrypted data)
  cli.py         # Command-line interface
```