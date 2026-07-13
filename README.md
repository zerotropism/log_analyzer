# Log Analyzer

Outil d'analyse de sécurité des logs en Python. Il analyse des fichiers de logs serveur pour détecter les comportements suspects, extraire des statistiques d'utilisation et générer des rapports JSON.

## Fonctionnalités

- **Parsing des logs** : lecture et validation du format `[TIMESTAMP] [LEVEL] [IP] [USER] ACTION: message`
- **Détection d'anomalies** : identification des sources (IP/utilisateur) générant plus de 5 erreurs en moins de 5 minutes
- **Requêtes** :
  - Nombre de connexions réussies par utilisateur
  - Liste des adresses IP par utilisateur
- **Rapport JSON** : résumé global + activités suspectes + statistiques de connexion
- **Mode streaming** : traitement ligne par ligne pour les fichiers volumineux (> 32 Go)
- **Robustesse** : les lignes mal formatées sont comptabilisées sans interrompre l'analyse

## Format de log attendu

- `[2024-01-15 10:23:45] [INFO] [192.168.1.100] [john_doe] LOGIN: Successful login attempt`
- `[2024-01-15 10:23:47] [ERROR] [192.168.1.101] [jane_smith] ACCESS: Invalid permission for /admin/users`

## Installation

Nécessite Python 3.12+.

```bash
uv sync
```

## Utilisation

```Python
# Analyse standard
python main.py --input input/server_activity.log

# Sauvegarde du rapport dans un fichier
python main.py --input input/server_activity.log --output rapport.json

# Mode streaming pour les fichiers volumineux (> 32 Go)
python main.py --input input/server_activity.log --large-file
```

## Structure du rapport de sortie

```json
{
  "summary": {
    "total_entries": 1500,
    "total_users": 12,
    "total_ips": 8,
    "malformed_entries": 3
  },
  "suspicious_activity": [
    {
      "ip": "192.168.1.101",
      "user": "jane_smith",
      "error_count": 7,
      "time_range": ["2024-01-15 10:20:00", "2024-01-15 10:24:30"]
    }
  ],
  "logins_per_user": {
    "john_doe": 5
  },
  "ips_per_user": {
    "john_doe": ["192.168.1.100", "10.0.0.5"]
  }
}
```

## Structure du projet

log_analyzer/
├── main.py               # Point d'entrée CLI
├── log_loader.py         # Chargement du fichier (mode DataFrame ou streaming)
├── log_parser.py         # Parsing des lignes de log
├── anomaly_detector.py   # Détection des rafales d'erreurs
├── queries.py            # Requêtes analytiques (connexions, IPs)
├── report.py             # Génération du rapport JSON
├── input/                # Fichiers de logs d'exemple
└── tests/                # Tests unitaires (pytest)

## Tests

```bash
pytest
```
