from produit import Produit
from client import Client
from commande import Commande

# --- Tests classe Produit ---
p1 = Produit("P01", "Plat du jour", "plat", 7.20, 20)
p2 = Produit("B01", "Café expresso", "boisson chaude", 1.20, 100)

print(p1)
print(repr(p2))

# Test du tri (__lt__)
assert p2 < p1, "Erreur: Le café devrait être moins cher que le plat"

# Tests de disponibilité
assert p2.est_disponible(150, "08:00") == False, "Erreur: Rupture de stock non détectée"
assert p1.est_disponible(1, "12:00") == True, "Erreur: Le plat devrait être dispo à midi"
assert p1.est_disponible(1, "14:00") == False, "Erreur: Le service des plats finit à 14h00 exclue"
assert p1.est_disponible(1, "11:29") == False, "Erreur: Le service des plats ne commence qu'à 11h30"

print("Tous les tests Produit sont validés !")

# --- Tests classe Client ---
c1 = Client("Alice", "étudiant", 12.0)
c2 = Client("Farid", "personnel", 0.0)
c3 = Client("Visiteur", "visiteur")

# Tests recharges
assert c1.recharger(20.0) == True
assert c1.solde == 32.0
assert c1.recharger(130.0) == False
assert c3.recharger(10.0) == False

# Tests paiement et découvert
assert c2.peut_payer(8.0) == True
assert c2.peut_payer(15.0) == False
assert c1.peut_payer(40.0) == False

# Tests fidélité (B1)
c1.points_fidelite = 32
remise = c1.calculer_avantage_fidelite(10.0)
assert remise == 2.0
assert c1.points_fidelite == 12

print("Tous les tests Produit sont validés !")

# --- Tests classe Commande ---
cafe = Produit("B01", "Café expresso", "boisson chaude", 1.20, 100)
croissant = Produit("V01", "Croissant", "viennoiserie", 1.20, 30)
client_test = Client("Alice", "étudiant", 12.0)

# Tests compteur de commandes
cmd1 = Commande(client_test, "07:45")
cmd2 = Commande(client_test, "08:10")
assert cmd1.numero == 1
assert cmd2.numero == 2

# Tests ajout de lignes
cmd1.ajouter_ligne(cafe, 1)
cmd1.ajouter_ligne(croissant, 2)
cmd1.ajouter_ligne(cafe, 1)

# Tests des méthodes magiques
assert len(cmd1) == 4
assert cafe in cmd1
assert len(cmd1.lignes) == 2

print("Tous les tests Commande (Partie 1) sont validés !")

# --- Tests classe Commande : Calcul du total (A2 + B1) et affichage ticket ---
plat = Produit("P01", "Plat du jour", "plat", 7.20, 20)

etu = Client("Alice", "étudiant", 20.0)
pers = Client("Farid", "personnel", 20.0)
vis = Client("Invité", "visiteur")

# 1. Happy Hour étudiant à 15h30 : 2 cafés à 1.20 € -> 2.40 * 0.80 = 1.92 €
cmd_hh = Commande(etu, "15:30")
cmd_hh.ajouter_ligne(cafe, 2)
assert cmd_hh.calculer_total() == 1.92

# 2. Fin exclue à 17h00 : plein tarif -> 2.40 €
cmd_fin_hh = Commande(etu, "17:00")
cmd_fin_hh.ajouter_ligne(cafe, 2)
assert cmd_fin_hh.calculer_total() == 2.40

# 3. Visiteur à 15h30
cmd_vis = Commande(vis, "15:30")
cmd_vis.ajouter_ligne(cafe, 1)
assert cmd_vis.calculer_total() == 1.20

# 4. Personnel à 15h30 (1 café + 1 plat) : (1.20 * 0.80 + 7.20) * 0.95 = 8.16 * 0.95 = 7.752 -> 7.75 €
cmd_pers = Commande(pers, "15:30")
cmd_pers.ajouter_ligne(cafe, 1)
cmd_pers.ajouter_ligne(plat, 1)
assert cmd_pers.calculer_total() == 7.75

# 5. Bon d'achat fidélité B1 (-2.00 €) + plancher à 0.0 €
etu.points_fidelite = 35
cmd_fidelite = Commande(etu, "10:00")
cmd_fidelite.ajouter_ligne(cafe, 1)  # 1.20 € - 2.00 € -> bloqué à 0.0 €
assert cmd_fidelite.calculer_total() == 0.0
assert etu.points_fidelite == 35

print(cmd_pers)
print("Tous les tests Commande (Partie 2) sont validés !")