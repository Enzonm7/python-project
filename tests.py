from produit import Produit
from client import Client
from commande import Commande
from cafeteria import Cafeteria

# --- Tests classe Produit ---
p1 = Produit("P01", "Plat du jour", "plat", 7.20, 20)
p2 = Produit("B01", "Café expresso", "boisson chaude", 1.20, 100)

print(p1)
print(repr(p2))

# Test du tri (__lt__) et de l'égalité sécurisée (__eq__)
assert p2 < p1, "Erreur: Le café devrait être moins cher que le plat"
assert not (p1 == "P01"), "Erreur: Un Produit ne doit pas être égal à une chaîne"

# Tests de disponibilité
assert not p2.est_disponible(150, "08:00"), "Erreur: Rupture de stock non détectée"
assert p1.est_disponible(1, "12:00"), "Erreur: Le plat devrait être dispo à midi"
assert not p1.est_disponible(1, "14:00"), "Erreur: Le service des plats finit à 14h00 exclue"
assert not p1.est_disponible(1, "11:29"), "Erreur: Le service des plats ne commence qu'à 11h30"

print("Tous les tests de Produit sont validés !")

# --- Tests classe Client ---
c1 = Client("Alice", "étudiant", 12.0)
c2 = Client("Farid", "personnel", 0.0)
c3 = Client("Visiteur", "visiteur")

# Tests recharges
assert c1.recharger(20.0)
assert c1.solde == 32.0
assert not c1.recharger(130.0)
assert not c3.recharger(10.0)

# Tests paiement et découvert
assert c2.peut_payer(8.0)
assert not c2.peut_payer(15.0)
assert not c1.peut_payer(40.0)

# Tests fidélité : seuil 29 puis 30 points + mise à jour
c1.points_fidelite = 29
assert not c1.a_droit_au_bon(), "Erreur: Pas de bon à 29 points"
c1.points_fidelite = 30
assert c1.a_droit_au_bon(), "Erreur: Bon dû à partir de 30 points"

c1.points_fidelite = 32
assert c1.a_droit_au_bon()
c1.actualiser_fidelite(10.0)
assert c1.points_fidelite == 12  # 32 - 30 + int(10.0) = 12

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

# --- Tests classe Commande : Calcul du total et affichage ticket ---
plat = Produit("P01", "Plat du jour", "plat", 7.20, 20)

etu = Client("Alice", "étudiant", 20.0)
pers = Client("Farid", "personnel", 20.0)
vis = Client("Invité", "visiteur")

# 1. Happy Hour étudiant à 15h00 inclus et 16h59 : 2 cafés à 1.20 € -> 2.40 * 0.80 = 1.92 €
cmd_debut_hh = Commande(etu, "15:00")
cmd_debut_hh.ajouter_ligne(cafe, 2)
assert cmd_debut_hh.calculer_total() == 1.92

cmd_fin_hh_incluse = Commande(etu, "16:59")
cmd_fin_hh_incluse.ajouter_ligne(cafe, 2)
assert cmd_fin_hh_incluse.calculer_total() == 1.92

# 2. Fin exclue à 17h00 : plein tarif -> 2.40 €
cmd_fin_hh = Commande(etu, "17:00")
cmd_fin_hh.ajouter_ligne(cafe, 2)
assert cmd_fin_hh.calculer_total() == 2.40

# 3. Visiteur à 15h30 (pas de Happy Hour)
cmd_vis = Commande(vis, "15:30")
cmd_vis.ajouter_ligne(cafe, 1)
assert cmd_vis.calculer_total() == 1.20

# 4. Personnel à 15h30 (1 café + 1 plat) : (1.20 * 0.80 + 7.20) * 0.95 = 8.16 * 0.95 = 7.752 -> 7.75 €
cmd_pers = Commande(pers, "15:30")
cmd_pers.ajouter_ligne(cafe, 1)
cmd_pers.ajouter_ligne(plat, 1)
assert cmd_pers.calculer_total() == 7.75

# 5. Bon d'achat fidélité (-2.00 €) + plancher à 0.0 €
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

assert cafet.traiter_commande(cmd_echec) == (False, "hors créneau", 0.0)
assert cafet.refus["hors créneau"] == 1
assert cafe_cafet.stock == 10       # Le stock du café n'a PAS été touché
assert alice_cafet.solde == 5.0       # Le solde n'a PAS été débité
assert cafet.chiffre_affaires == 0.0  # La caisse reste à 0

# 2. Test refus faute de solde : 1 plat à 7.20 € à 12h30 avec 5.0 € sur le badge
cmd_pauvre = Commande(alice_cafet, "12:30")
cmd_pauvre.ajouter_ligne(plat_cafet, 1)
assert cafet.traiter_commande(cmd_pauvre) == (False, "solde insuffisant", 0.0)
assert cafet.refus["solde insuffisant"] == 1
assert plat_cafet.stock == 5

# 3. Test validation complète : 2 cafés à 15h30 (Happy Hour : 2.40 * 0.80 = 1.92 €)
cmd_ok = Commande(alice_cafet, "15:30")
cmd_ok.ajouter_ligne(cafe_cafet, 2)
assert cafet.traiter_commande(cmd_ok) == (True, "acceptée", 1.92)
assert cafe_cafet.stock == 8
assert round(alice_cafet.solde, 2) == 3.08
assert alice_cafet.points_fidelite == 1   # int(1.92) = 1 point gagné
assert cafet.chiffre_affaires == 1.92
assert cafet.total_remises == 0.48        # 2.40 - 1.92 = 0.48 € de remise
assert len(cafet.commandes) == 1

# 4. Test des motifs de refus (rupture, inconnu, commande vide, quantité négative parmi d'autres lignes)
cmd_rupture = Commande(alice_cafet, "10:00")
cmd_rupture.ajouter_ligne(cafe_cafet, 9)  # Stock actuel = 8
assert cafet.traiter_commande(cmd_rupture) == (False, "rupture de stock", 0.0)
assert cafet.refus["rupture de stock"] == 1

smoothie = Produit("S01", "Smoothie mangue", "boisson froide", 3.00, 5)
cmd_inconnu = Commande(alice_cafet, "10:00")
cmd_inconnu.ajouter_ligne(smoothie, 1)    # Non ajouté au catalogue
assert cafet.traiter_commande(cmd_inconnu) == (False, "produit inconnu", 0.0)
assert cafet.refus["produit inconnu"] == 1

cmd_vide = Commande(alice_cafet, "10:00")
assert cafet.traiter_commande(cmd_vide) == (False, "quantité invalide", 0.0)
assert cafet.refus["quantité invalide"] == 1

cmd_qte_neg = Commande(alice_cafet, "10:00")
cmd_qte_neg.ajouter_ligne(cafe_cafet, 1)
cmd_qte_neg.ajouter_ligne(plat_cafet, -2)
assert cafet.traiter_commande(cmd_qte_neg) == (False, "quantité invalide", 0.0)
assert cafet.refus["quantité invalide"] == 2

# 5. Tests de recharge (plafond exact 100.00 €) et réapprovisionnement
assert cafet.recharger_badge("Alice", 100.00) == (True, "recharge acceptée")
assert round(alice_cafet.solde, 2) == 103.08
assert cafet.reapprovisionner("B01", 2)
assert cafe_cafet.stock == 10

# 6. Cas limites : heure 11:30 incluse, solde exact, stock exact et -5 % personnel hors Happy Hour
bob_cafet = Client("Bob", "alternant", 7.20)
cafet.inscrire_client(bob_cafet)
cmd_exact = Commande(bob_cafet, "11:30")
cmd_exact.ajouter_ligne(plat_cafet, 1)
assert cafet.traiter_commande(cmd_exact) == (True, "acceptée", 7.20)
assert bob_cafet.solde == 0.0

farid_cafet = Client("Farid", "personnel", 1.40)
cafet.inscrire_client(farid_cafet)
cmd_decouvert = Commande(farid_cafet, "10:00")
cmd_decouvert.ajouter_ligne(cafe_cafet, 10)  # 12.00 * 0.95 = 11.40 € -> solde = -10.00 €
assert cafet.traiter_commande(cmd_decouvert) == (True, "acceptée", 11.40)
assert round(farid_cafet.solde, 2) == -10.00
assert cafe_cafet.stock == 0

# 7. Cohérence du ticket avec le montant payé après déduction des points de fidélité
assert cafet.reapprovisionner("B01", 5)
alice_cafet.points_fidelite = 30
cmd_ticket = Commande(alice_cafet, "10:00")
cmd_ticket.ajouter_ligne(cafe_cafet, 1)  # 1.20 € - 2.00 € (bon) = 0.00 €
assert cafet.traiter_commande(cmd_ticket) == (True, "acceptée", 0.0)
assert alice_cafet.points_fidelite == 0  # Les 30 points ont bien été consommés
assert "TOTAL À PAYER : 0.00 €" in str(cmd_ticket)

# 8. Produit de même code mais instance différente : vérifie l'utilisation du produit de la carte
cafe_autre_objet = Produit("B01", "Café expresso", "boisson chaude", 1.20, 999)
cmd_autre_obj = Commande(alice_cafet, "10:00")
cmd_autre_obj.ajouter_ligne(cafe_autre_objet, 2)
assert cafet.traiter_commande(cmd_autre_obj) == (True, "acceptée", 2.40)
assert cafe_cafet.stock == 2        # Le stock officiel (4 - 2 = 2) a bien diminué
assert cafe_autre_objet.stock == 999  # L'objet externe n'a pas été touché

print("Tous les tests de Cafeteria sont validés !")

# --- Tests Phase 1 : Annulation de commande ---
cafet_p1 = Cafeteria("Cafétéria Phase 1")
cafe_p1 = Produit("B01", "Café expresso", "boisson chaude", 1.20, 10)
wrap_p1 = Produit("W01", "Wrap végétarien", "plat", 4.60, 9)
cafet_p1.ajouter_produit(cafe_p1)
cafet_p1.ajouter_produit(wrap_p1)

chloe_p1 = Client("Chloé", "étudiant", 14.40)
chloe_p1.points_fidelite = 10
cafet_p1.inscrire_client(chloe_p1)

visiteur_p1 = Client("Paul", "visiteur")
cafet_p1.inscrire_client(visiteur_p1)

# 1. Dernière commande annulée -> retour exact à l'état d'avant (solde, stock, fidélité)
solde_avant = chloe_p1.solde
points_avant = chloe_p1.points_fidelite
stock_wrap_avant = wrap_p1.stock

cmd_chloe = Commande(chloe_p1, "12:18")
cmd_chloe.ajouter_ligne(wrap_p1, 1)
assert cafet_p1.traiter_commande(cmd_chloe) == (True, "acceptée", 4.60)
assert round(chloe_p1.solde, 2) == 9.80
assert chloe_p1.points_fidelite == 14
assert wrap_p1.stock == 8

ok_annul, motif_annul, remb_annul = cafet_p1.annuler_commande(cmd_chloe.numero)
assert ok_annul is True
assert motif_annul == "annulée"
assert remb_annul == 4.60
assert round(chloe_p1.solde, 2) == round(solde_avant, 2)
assert chloe_p1.points_fidelite == points_avant
assert wrap_p1.stock == stock_wrap_avant
assert cmd_chloe.statut == "annulée"

# 2. Annulation d'une commande inconnue
solde_avant_inconnu = chloe_p1.solde
stock_avant_inconnu = wrap_p1.stock
points_avant_inconnu = chloe_p1.points_fidelite
assert cafet_p1.annuler_commande(999) == (False, "commande inconnue", 0.0)
assert round(chloe_p1.solde, 2) == round(solde_avant_inconnu, 2)
assert wrap_p1.stock == stock_avant_inconnu
assert chloe_p1.points_fidelite == points_avant_inconnu

# 3 & 4. Annulation d'une commande déjà annulée -> refusée, rien n'est modifié
solde_avant_double = chloe_p1.solde
stock_avant_double = wrap_p1.stock
points_avant_double = chloe_p1.points_fidelite
assert cafet_p1.annuler_commande(cmd_chloe.numero) == (False, "commande déjà annulée", 0.0)
assert round(chloe_p1.solde, 2) == round(solde_avant_double, 2)
assert wrap_p1.stock == stock_avant_double
assert chloe_p1.points_fidelite == points_avant_double

# 5. Remboursement d'un visiteur (pas de solde de badge à modifier)
cmd_vis = Commande(visiteur_p1, "10:00")
cmd_vis.ajouter_ligne(cafe_p1, 2)  # 2.40 € comptant
assert cafet_p1.traiter_commande(cmd_vis) == (True, "acceptée", 2.40)
assert cafet_p1.annuler_commande(cmd_vis.numero) == (True, "annulée", 2.40)
assert visiteur_p1.solde == 0.0
assert visiteur_p1.points_fidelite == 0

# 6. Remboursement qui fait dépasser 150,00 € (plafond de recharge non appliqué)
chloe_p1.solde = 148.00
cmd_plafond = Commande(chloe_p1, "10:00")
cmd_plafond.ajouter_ligne(cafe_p1, 3)  # 3.60 € -> solde 144.40 €
assert cafet_p1.traiter_commande(cmd_plafond) == (True, "acceptée", 3.60)
chloe_p1.solde = 149.00
assert cafet_p1.annuler_commande(cmd_plafond.numero) == (True, "annulée", 3.60)
assert round(chloe_p1.solde, 2) == 152.60

# 7. Annulation d'une commande ayant utilisé un avantage de fidélité
chloe_p1.points_fidelite = 30
cmd_bon = Commande(chloe_p1, "10:00")
cmd_bon.ajouter_ligne(wrap_p1, 1)  # 4.60 € - 2.00 € (bon) = 2.60 €
assert cafet_p1.traiter_commande(cmd_bon) == (True, "acceptée", 2.60)
assert chloe_p1.points_fidelite == 2  # (30 - 30) + int(2.60) = 2
assert cafet_p1.annuler_commande(cmd_bon.numero) == (True, "annulée", 2.60)
assert chloe_p1.points_fidelite == 10  # Rejeu des commandes valides précédentes

# 8. Ticket d'une commande annulée
assert "ANNULÉE" in str(cmd_chloe)

print("Tous les tests de la Phase 1 sont validés !")