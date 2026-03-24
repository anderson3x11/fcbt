from dataclasses import dataclass

@dataclass
class Entry:
  service: str
  login: str
  password: str
  notes: str
  created_at: str #(format "2025-01-10")
  updated_at: str #(format "2025-01-10")

@dataclass
class Vault:
    entries: list[Entry]