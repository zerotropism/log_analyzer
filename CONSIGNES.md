# Test Technique Python - Analyse de Sécurité des Logs

## Contexte

Vous êtes responsable de la sécurité IT d'une entreprise. On vous fournit un fichier de logs contenant les activités des utilisateurs sur le système. Votre mission est de créer un outil d'analyse pour détecter les comportements suspects et générer des rapports de sécurité.

## Les données

Le fichier de logs contient des entrées au format :

[TIMESTAMP] [LEVEL] [IP] [USER] ACTION: message

Exemple :

[2024-01-15 10:23:45] [INFO] [192.168.1.100] [john_doe] LOGIN: Successful login attempt 

[2024-01-15 10:23:47] [ERROR] [192.168.1.101] [jane_smith] ACCESS: Invalid permission for /admin/users

## Objectif

Créer un programme Python qui permet d'analyser ces fichiers de logs pour :

1\. Identifier les activités suspectes plusieurs erreurs, superieur a 5 erreurs provenant de la même source (ip ou user) dans un court intervalle 5 min

2\. Permettre des recherches et filtres sur les événements

    1\. Récupérez le nombre de connexion réussies par user. 

    2\. Récupérez la liste des ip de connexion par user.

## Contraintes techniques

- Les fichiers de logs peuvent contenir des lignes mal formatées ou corrompues.

- Le format de sortie des rapports doit être en JSON.

- Le code doit être maintenable.

## Données de test

Un fichier exemple `server_activity.log` est fourni avec différents scénarios :

- Connexions réussies et échouées

- Tentatives d'accès non autorisés

- Erreurs applicatives

- Lignes mal formatées

## Livrable attendu

- Code source Python

## Points d'attention

- Qualité et lisibilité du code

- Gestion des cas d'erreur

- Performance et utilisation des ressources

- Facilité d'extension du code

## Bonus

- Le programme doit pouvoir traiter des fichiers volumineux. (plus que 32 GB) 

- tests unitaires sur une fonctionalité