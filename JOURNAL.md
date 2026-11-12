## Difficultés rencontrées et ce que j'en retiens

### 06-11-2026 : Classe Produit
- **Modification d'état de l'objet** : j'ai d'abord confondu le renvoi d'un calcul (`return self.stock - quantite`) avec la modification réelle de l'attribut de l'instance. J'ai corrigé cela en utilisant l'opérateur d'assignation (`self.stock -= quantite`) pour mettre à jour l'objet.
- **Méthodes magiques et sens de tri** : j'ai utilisé l'opérateur `>` pour la méthode `__lt__` (*Less Than*). J'ai compris que pour que la fonction `sorted()` trie la carte par prix croissant, il fallait utiliser `<`.
- **Syntaxe de base** : quelques coquilles corrigées (confusion entre l'assignation `=` et l'égalité `==` dans un `if`, et casse de la valeur `True`).
- **Pièges de la logique booléenne** (méthode `est_disponible`) : j'avais du mal à combiner les conditions de stock et d'horaire sans créer de bugs ou de courts-circuits avec l'opérateur `or`. J'ai résolu le problème en adoptant des « clauses de garde » : j'élimine d'abord le cas du stock insuffisant (`return False`), puis le cas du plat commandé hors créneau (`return False`). Si le code survit à ces deux filtres, c'est que le produit est disponible (`return True`). C'est beaucoup plus lisible et sécurisé.

### 09-11-2026 : Classe Produit
- **Automatisation des tests** : découverte et implémentation de l'instruction `assert` pour valider silencieusement mon code face aux cas limites.

### 10-11-2026 : Classe Client:
- **Initialisation des objets** (classe `Client`) : j'ai compris la différence entre un attribut passé en paramètre avec une valeur par défaut (le `solde` à `0.0`, car certains clients démarrent la journée avec de l'argent) et un attribut initialisé en dur dans la méthode (les `points_fidelite` à `0`, car aucun client ne commence avec des points).
- **Structure des conditions** (`if` en cascade vs `elif`) : j'avais d'abord utilisé une boucle `while` dans `recharger` et mélangé des conditions dans `peut_payer`. J'ai appris à distinguer les clauses de garde en cascade (`if` successifs dans `se_recharger` pour éliminer chaque cas de refus : visiteur, montant hors [5 €, 100 €], dépassement du plafond de 150 €) des aiguillages mutuellement exclusifs (`elif` dans `peut_payer` selon le profil du client).
- **Priorité des opérateurs** (`and` / `or` et comparaisons) : j'ai corrigé un bug logique dans `peut_payer` où l'évaluation prioritaire du `and` sur le `or` autorisait un étudiant à payer même avec un solde nul. J'ai également noté que les calculs arithmétiques (`-`) s'exécutent toujours avant les comparaisons (`>=`), et que les parenthèses autour de `(self.solde - montant)` servent avant tout à clarifier la lecture du code.
 
### 11-11-2026 : Classe Client:
- **Types de retour et précision des nombres flottants** : j'ai remplacé les retours en chaînes de caractères (`"Accepté"` / `"Refusé"`) par des booléens (`True` / `False`) pour rendre les méthodes exploitables par la future classe `Cafeteria`.
- **Implémentation de la variante B1** (fidélité) : j'ai structuré `calculer_avantage_fidelite` en vérifiant d'abord si le client possède au moins 30 points pour appliquer la remise de 2,00 € (et retirer 30 points), avant d'ajouter les nouveaux points acquis sur la commande (`int(montant_paye)`), tout en excluant le profil visiteur.