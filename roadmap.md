# First City Bank and Trust — Spécifications du projet

## Concept

Gestionnaire de mots de passe en ligne de commande avec interface TUI (Terminal User Interface), orienté portfolio cyber. Projet personnel et utilisable au quotidien. Compatible Windows, Linux et macOS.

---

## Flux utilisateur

### Première utilisation
```
$ fcbt
→ Aucun coffre détecté
→ Créer un mot de passe maître
→ Confirmer
→ vault.enc créé dans le dossier utilisateur
→ Accès au menu principal
```

### Utilisation courante
```
$ fcbt
→ Saisir le mot de passe maître
→ Déchiffrement du coffre en mémoire
→ Menu principal TUI
```

---

## Installation et distribution

Le projet utilise `pyproject.toml` avec un **entry point console** :

```toml
[project.scripts]
fcbt = "fcbt.app:main"
```

Après `pip install .` (ou `pip install -e .` en dev), la commande `fcbt` est disponible globalement dans le terminal.

### Emplacement des données utilisateur

Le fichier `vault.enc` est stocké dans le dossier standard de chaque OS (géré via `platformdirs`) :

| OS | Emplacement |
|---|---|
| **Linux** | `~/.local/share/fcbt/vault.enc` |
| **macOS** | `~/Library/Application Support/fcbt/vault.enc` |
| **Windows** | `%LOCALAPPDATA%\fcbt\vault.enc` |

---

## Interface TUI

Menu principal interactif navigable au clavier (via `textual`) :

```
┌─────────────────────────────────────┐
│  FCBT                               │
├─────────────────────────────────────┤
│  [1] Rechercher un mot de passe     │
│  [2] Ajouter une entrée            │
│  [3] Modifier une entrée           │
│  [4] Supprimer une entrée          │
│  [5] Générer un mot de passe       │
│  [6] Changer le mot de passe maître│
│  [7] Quitter                       │
└─────────────────────────────────────┘
```

---

## Modèle de données

Chaque entrée est identifiée par le couple **(service, login)** — un même service peut avoir plusieurs logins distincts.

```json
{
  "entries": [
    {
      "service": "github.com",
      "login": "thomas@mail.com",
      "password": "X7#mK9$pLq2!nR4v",
      "notes": "",
      "created_at": "2025-01-10",
      "updated_at": "2025-01-10"
    },
    {
      "service": "github.com",
      "login": "pro@entreprise.com",
      "password": "aZ2!qW9#mP5$nL8v",
      "notes": "compte pro — 2FA activé",
      "created_at": "2025-01-12",
      "updated_at": "2025-01-12"
    }
  ]
}
```

> Plusieurs logins (et donc plusieurs mots de passe) peuvent coexister pour un même service. La clé unique d'une entrée est le couple `(service, login)`.

---

## Architecture cryptographique

```
Mot de passe maître (saisi par l'utilisateur)
          ↓
      [Argon2id]  ←  sel aléatoire 16 bytes (stocké en clair dans vault.enc)
          ↓
      Clé 256 bits
          ↓
      [AES-256-GCM]  ←  IV aléatoire 12 bytes (stocké en clair dans vault.enc)
          ↓
   Données chiffrées + tag d'authentification (AEAD)
          ↓
        vault.enc
```

**Structure de `vault.enc` :**
```
[sel Argon2 : 16 bytes][IV AES-GCM : 12 bytes][ciphertext + tag GCM]
```

### Pourquoi ces choix ?

| Choix | Raison |
|---|---|
| **Argon2id** | Résistant aux attaques GPU/ASIC, recommandé par OWASP |
| **AES-256-GCM** | Chiffrement authentifié (AEAD) : confidentialité + intégrité en un seul algo |
| **Pas de SHA-256 direct** | SHA-256 seul n'est pas une KDF — trop rapide à brute-forcer |
| **Sel et IV aléatoires** | Évite les attaques par rainbow table et les réutilisations de clé |

---

## Fonctionnalités

### MVP — V1

- [ ] Création du coffre avec mot de passe maître
- [ ] Chiffrement AES-256-GCM + dérivation Argon2id
- [ ] Ajouter une entrée (service + login + mot de passe)
- [ ] Rechercher une entrée par service (affiche tous les logins associés)
- [ ] Afficher / copier un mot de passe
- [ ] Générateur de mots de passe robuste (longueur, jeu de caractères configurable)
- [ ] Interface TUI avec `textual`

### V2 — Améliorations

- [ ] Modifier une entrée existante
- [ ] Supprimer une entrée
- [ ] Changer le mot de passe maître
- [ ] Copie dans le presse-papier avec effacement automatique après 30s
- [ ] Champ notes optionnel par entrée
- [ ] Verrouillage automatique après inactivité (timeout configurable)

### V3 — Fonctionnalités avancées

- [ ] Vérification HIBP (Have I Been Pwned) via API k-anonymity
- [ ] Export chiffré (backup portable)
- [ ] Import depuis un backup chiffré

---

## Structure du projet

```
fcbt/
├── __init__.py
├── __main__.py       # Permet `python -m fcbt`
├── app.py            # Point d'entrée, TUI principale (textual)
├── crypto.py         # Chiffrement, déchiffrement, dérivation de clé
├── storage.py        # Lecture/écriture de vault.enc, gestion des chemins OS
├── generator.py      # Générateur de mots de passe
├── models.py         # Dataclasses (Entry, Vault)
├── pyproject.toml    # Config projet + entry point console
├── .gitignore        # vault.enc, __pycache__, .venv, etc.
└── README.md         # Threat model + documentation
```

> `vault.enc` n'est PAS dans le dossier projet — il est dans le dossier utilisateur (voir section Installation).

---

## Threat model (à documenter dans le README)

### Ce que FCBT protège
- Mots de passe au repos sur disque (fichier volé, accès physique)
- Lecture du fichier `vault.enc` sans le mot de passe maître

### Ce que FCBT ne protège pas
- Un keylogger actif sur la machine (capture du mot de passe maître)
- Un attaquant avec accès root (dump mémoire pendant la session)
- La robustesse du mot de passe maître lui-même (responsabilité utilisateur)
- Les mots de passe une fois affichés à l'écran

### Limites connues de Python
- Le garbage collector ne garantit pas l'effacement immédiat des secrets en mémoire. Les données sensibles (clé dérivée, mots de passe déchiffrés) peuvent persister en RAM après usage. Cette limitation est documentée par transparence.

---

## Dépendances Python

```
cryptography>=42.0      # AES-GCM, primitives crypto
argon2-cffi>=23.0       # Dérivation de clé Argon2id
textual>=0.50           # Framework TUI
platformdirs>=4.0       # Chemins OS-spécifiques (données utilisateur)
pyperclip>=1.8          # Copie presse-papier (V2)
```
