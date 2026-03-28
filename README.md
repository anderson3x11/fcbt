# FCBT - First City Bank and Trust

**A locally encrypted password manager built from scratch in Python.**

Your passwords never leave your machine. The vault is encrypted at rest with AES (Fernet) using PBKDF2 key derivation.

---

## Why FCBT?

Most password managers require trusting a third party with your secrets. FCBT takes a different approach:

- **Zero network access** -- your vault lives on your machine
- **Strong encryption** -- AES-128 via Fernet with PBKDF2-SHA256 (100,000 iterations)
- **Minimal dependencies** -- only `cryptography` and `pyperclip`, everything else is stdlib

---

## Features

| Feature | Description |
|---|---|
| **Encrypted vault** | AES via Fernet + PBKDF2 key derivation with per-save random salt |
| **CRUD operations** | Add, search, modify, and delete password entries |
| **Password generator** | Cryptographically secure generation via `secrets` (configurable length & charset) |
| **Master password** | Change it anytime -- the vault is re-encrypted transparently |
| **Clipboard copy** | Copy passwords to clipboard with auto-clear after 30 seconds |
| **Auto-lock** | Vault locks after 2 minutes of inactivity |
| **First-run setup** | Guided vault creation with master password confirmation |
| **Colored CLI** | Clean terminal UI with visual feedback and navigation |

---

## Screenshots

<p align="center">
  <img src="assets/Menu.png" alt="Main menu" width="800">
  <img src="assets/Add Entry.png" alt="Add entry with password generation" width="400">
  <img src="assets/Search.png" alt="Search entry" width="400">
</p>

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Encryption | `cryptography` (Fernet / AES-128-CBC + HMAC) |
| Key Derivation | PBKDF2-HMAC-SHA256, 100k iterations, 16-byte random salt |
| Random Source | `secrets` (CSPRNG) |
| Data Layer | JSON serialization, flat-file storage (`vault.dat`) |

---

## Architecture

```
fcbt/
  __main__.py    # Entry point for `python -m fcbt`
  models.py      # Entry & Vault dataclasses
  crypto.py      # Key derivation (PBKDF2) + encrypt/decrypt (Fernet)
  generator.py   # Cryptographically secure password generation
  storage.py     # Vault persistence (salt + ciphertext in a single file)
  cli.py         # Interactive terminal interface
```

**Data flow:**

```
Master password
      |
      v
  PBKDF2-SHA256 (100k rounds + random salt)
      |
      v
  AES key (Fernet)
      |
      v
  Encrypt/Decrypt vault (JSON <-> bytes)
      |
      v
  vault.dat (salt || ciphertext)
```

---

## Security Model

| Property | Implementation |
|---|---|
| Encryption at rest | Fernet (AES-128-CBC + HMAC-SHA256) |
| Key derivation | PBKDF2-HMAC-SHA256, 100,000 iterations |
| Salt | 16 bytes, regenerated on every save |
| Authenticated encryption | Fernet provides integrity + confidentiality |
| Secure random | `secrets` module (OS-level CSPRNG) |
| No plaintext on disk | Vault is always encrypted before writing |

---

## Getting Started

### Prerequisites

- Python 3.10+

### Installation (global, recommended)

```bash
git clone https://github.com/anderson3x11/fcbt.git
cd fcbt
pipx install .
```

The `fcbt` command will be available globally from any terminal.

To update to the latest version:

```bash
cd fcbt
git pull
pipx install . --force
```

### Installation (dev)

```bash
git clone https://github.com/anderson3x11/fcbt.git
cd fcbt
python -m venv .venv
.venv\Scripts\activate         # Windows
# source .venv/bin/activate    # Linux/macOS
pip install -e .
```

### Usage

```bash
fcbt
```

On first launch, you'll be asked to create a vault and set a master password.
On subsequent launches, enter your master password to unlock the existing vault.

### Vault location

The encrypted vault is stored in `~/.fcbt/vault.dat`:

| OS | Path |
|---|---|
| Windows | `C:\Users\<user>\.fcbt\vault.dat` |
| Linux | `/home/<user>/.fcbt/vault.dat` |
| macOS | `/Users/<user>/.fcbt/vault.dat` |