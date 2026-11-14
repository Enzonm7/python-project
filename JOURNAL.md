## Difficultés rencontrées et ce que j'en retiens

### 06-11-2026 : Classe Produit
- **Modification d'état de l'objet** : j'ai d'abord confondu le renvoi d'un calcul (`return self.stock - quantite`) avec la modification réelle de l'attribut de l'instance. J'ai corrigé cela en utilisant l'opérateur d'assignation (`self.stock -= quantite`) pour mettre à jour l'objet.
- **Méthodes magiques et sens de tri** : j'ai utilisé l'opérateur `>` pour la méthode `__lt__` (*Less Than*). J'ai compris que pour que la fonction `sorted()` trie la carte par prix croissant, il fallait utiliser `<`.
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

### 12-11-2026 : Classe Commande:
- **Hachage d'objets (`__hash__`)** : en utilisant une instance de `Produit` comme clé dans le dictionnaire `self.lignes` de `Commande`, j'ai rencontré une erreur `TypeError: unhashable type: 'Produit'`. J'ai compris que redéfinir `__eq__` sur `Produit` supprime son empreinte par défaut en Python ; l'ajout de `def __hash__(self): return hash(self.code)` a permis d'autoriser son utilisation comme clé de dictionnaire.
- **Exécution parasite lors des imports** : en séparant mes classes dans des fichiers distincts (`produit.py`, `client.py`, `commande.py`), j'ai constaté que les `assert` et `print` laissés en bas de chaque fichier s'exécutaient en double lors des imports croisés. J'ai résolu ce problème en centralisant tous mes tests dans un fichier `tests.py` dédié.

### 13-11-2026 : Classe Commande:
- **Ordre d'application des remises (variantes A2 et B1)** : j'avais d'abord mélangé la remise personnel (-5 %) et l'Happy Hour (-20 %) dans la même boucle en utilisant un `for` sur les catégories au lieu d'un `if`. En relisant la règle A2, j'ai séparé `calculer_total` en trois étapes : d'abord le calcul ligne par ligne avec les -20 % Happy Hour sur les boissons (15h00–17h00, hors visiteur), ensuite les -5 % du personnel sur le total global, et enfin la déduction du bon d'achat fidélité (-2,00 € si ≥ 30 points) sans débiter les points avant la validation réelle du paiement.
- **Construction dynamique du ticket (`__str__`)** : contrairement à `Produit` qui possède un nombre fixe d'attributs, une commande contient un nombre variable d'articles. J'ai opté pour une construction progressive par concaténation (`ticket += ...`) dans une boucle, afin de garder un code simple à lire et facile à modifier.