from produit import Produit
from client import Client
from commande import Commande
from cafeteria import Cafeteria

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

print("Tous les tests de Produit sont validés !")

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

print("Tous les tests de Client sont validés !")

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

print("Tous les tests de Commande (Partie 1) sont validés !")

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
print("Tous les tests de Commande (Partie 2) sont validés !")

# --- Tests classe Cafeteria ---
cafet = Cafeteria("Cafétéria Centrale")
cafe_cafet = Produit("B01", "Café expresso", "boisson chaude", 1.20, 10)
plat_cafet = Produit("P01", "Plat du jour", "plat", 7.20, 5)
cafet.ajouter_produit(cafe_cafet)
cafet.ajouter_produit(plat_cafet)

alice_cafet = Client("Alice", "étudiant", 5.0)
cafet.inscrire_client(alice_cafet)

# 1. Test "tout ou rien" : 1 café (dispo) + 1 plat à 10h00 (motif : hors créneau)
cmd_echec = Commande(alice_cafet, "10:00")
cmd_echec.ajouter_ligne(cafe_cafet, 1)
cmd_echec.ajouter_ligne(plat_cafet, 1)

assert cafet.valider_commande(cmd_echec) == (False, "hors créneau", 0.0)
assert cafet.refus["hors créneau"] == 1
assert cafe_cafet.stock == 10       # Le stock du café n'a PAS été touché
assert alice_cafet.solde == 5.0       # Le solde n'a PAS été débité
assert cafet.chiffre_affaires == 0.0  # La caisse reste à 0

# 2. Test refus faute de solde : 1 plat à 7.20 € à 12h30 avec 5.0 € sur le badge
cmd_pauvre = Commande(alice_cafet, "12:30")
cmd_pauvre.ajouter_ligne(plat_cafet, 1)
assert cafet.valider_commande(cmd_pauvre) == (False, "solde insuffisant", 0.0)
assert cafet.refus["solde insuffisant"] == 1
assert plat_cafet.stock == 5

# 3. Test validation complète : 2 cafés à 15h30 (Happy Hour : 2.40 * 0.80 = 1.92 €)
cmd_ok = Commande(alice_cafet, "15:30")
cmd_ok.ajouter_ligne(cafe_cafet, 2)
assert cafet.valider_commande(cmd_ok) == (True, "acceptée", 1.92)
assert cafe_cafet.stock == 8
assert round(alice_cafet.solde, 2) == 3.08
assert alice_cafet.points_fidelite == 1   # int(1.92) = 1 point gagné
assert cafet.chiffre_affaires == 1.92
assert cafet.total_remises == 0.48        # 2.40 - 1.92 = 0.48 € de remise
assert len(cafet.commandes) == 1

# 4. Test des 3 autres motifs de refus (rupture, inconnu, quantité invalide)
cmd_rupture = Commande(alice_cafet, "10:00")
cmd_rupture.ajouter_ligne(cafe_cafet, 9)  # Stock actuel = 8
assert cafet.valider_commande(cmd_rupture) == (False, "rupture de stock", 0.0)
assert cafet.refus["rupture de stock"] == 1

smoothie = Produit("S01", "Smoothie mangue", "boisson froide", 3.00, 5)
cmd_inconnu = Commande(alice_cafet, "10:00")
cmd_inconnu.ajouter_ligne(smoothie, 1)    # Non ajouté au catalogue
assert cafet.valider_commande(cmd_inconnu) == (False, "produit inconnu", 0.0)
assert cafet.refus["produit inconnu"] == 1

cmd_vide = Commande(alice_cafet, "10:00")
assert cafet.valider_commande(cmd_vide) == (False, "quantité invalide", 0.0)
assert cafet.refus["quantité invalide"] == 1

# 5. Tests de recharge (plafond exact 100.00 €) et réapprovisionnement
assert cafet.recharger_badge("Alice", 100.00) == (True, "recharge acceptée")
assert round(alice_cafet.solde, 2) == 103.08
assert cafet.reapprovisionner("B01", 2) == True
assert cafe_cafet.stock == 10

# 6. Cas limites : heure 11:30 incluse, solde exact, stock exact et découvert à -10.00 €
bob_cafet = Client("Bob", "alternant", 7.20)
cafet.inscrire_client(bob_cafet)
cmd_exact = Commande(bob_cafet, "11:30")
cmd_exact.ajouter_ligne(plat_cafet, 1)
assert cafet.valider_commande(cmd_exact) == (True, "acceptée", 7.20)
assert bob_cafet.solde == 0.0

farid_cafet = Client("Farid", "personnel", 1.40)
cafet.inscrire_client(farid_cafet)
cmd_decouvert = Commande(farid_cafet, "10:00")
cmd_decouvert.ajouter_ligne(cafe_cafet, 10)  # 12.00 * 0.95 = 11.40 € -> solde = -10.00 €
assert cafet.valider_commande(cmd_decouvert) == (True, "acceptée", 11.40)
assert round(farid_cafet.solde, 2) == -10.00
assert cafe_cafet.stock == 0

print("Tous les tests de Cafeteria sont validés !")