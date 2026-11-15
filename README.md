# CampusCafé

## Variante retenue
- **Axe A — A2 (Happy hour)** : Les titulaires d'un badge obtiennent 20 % de réduction sur les boissons entre 15:00 et 17:00 (fin exclue). Le personnel bénéficie de 5 % de réduction sur le total de sa commande à toute heure.
- **Axe B — B1 (Points)** : Le client gagne 1 point par euro entier payé. Dès qu'il atteint 30 points, sa commande suivante reçoit une remise de 2,00 € et 30 points sont retirés de son compte.

## Présentation du projet
Ce programme gère la caisse d'une cafétéria universitaire en Python (version 3.10 ou supérieure, sans bibliothèque externe). Il enregistre les produits de la carte et les badges des clients. Il contrôle chaque commande, applique les remises, met à jour les stocks et produit le rapport de fin de journée.

## Lancement du programme

### Exécuter les tests unitaires
Ouvrez un terminal dans le dossier du projet et lancez la commande suivante :
```bash
python tests.py
```
Le script vérifie le bon fonctionnement des quatre classes et affiche un message de confirmation.

### Exécuter le scénario de la journée
Lancez la commande suivante pour dérouler les 17 événements de la journée et afficher le rapport de clôture :
```bash
python main.py
```

Pour enregistrer ce résultat dans le fichier livrable :
```bash
python main.py > sortie_scenario.txt
```

## Organisation du projet
Le projet sépare les responsabilités dans plusieurs fichiers simples :
- `produit.py` : Contient la classe `Produit`. Elle gère le prix, le stock et les horaires de service des plats (de 11:30 à 14:00).
- `client.py` : Contient la classe `Client`. Elle gère le profil, le solde du badge, les recharges et les points de fidélité.
- `commande.py` : Contient la classe `Commande`. Elle regroupe les articles demandés, calcule le montant à payer et prépare l'affichage du ticket.
- `cafeteria.py` : Contient la classe `Cafeteria`. Elle centralise la carte, les clients, la validation des commandes et le rapport de clôture.
- `tests.py` : Contient les tests automatiques qui vérifient les règles et les cas limites.
- `main.py` : Rejoue la journée complète de service étape par étape.
- `conception/` : Contient les schémas papier et les calculs réalisés à la main.
- `JOURNAL.md` : Présente les difficultés rencontrées et les solutions apportées.
- `sortie_scenario.txt` : Contient le résultat complet de l'exécution de `main.py`.

## Choix de conception
- **Un fichier par classe** : Chaque classe possède son propre fichier pour faciliter la lecture et la maintenance du code.
- **Centralisation des règles** : Les seuils (horaires, plafond de recharge, découvert, taux de remise) sont placés en haut des classes. Cette organisation évite les valeurs cachées dans le code et simplifie les modifications.
- **Traitement en « tout ou rien »** : La cafétéria vérifie toutes les conditions d'une commande avant de modifier les stocks ou le solde du client. Si une vérification échoue, le programme annule l'opération et enregistre le motif exact du refus.
- **Séparation entre calcul et mise à jour** : Le calcul du prix vérifie uniquement si le client possède 30 points sans les retirer. Le programme retire les points et mémorise le montant payé uniquement après la validation du paiement.
- **Tri simple sans fonction anonyme** : Pour classer les trois produits les plus vendus, le programme place la quantité en premier dans une liste de paires `(quantité, nom)`. La fonction `sorted()` trie ainsi les ventes naturellement du plus grand au plus petit.