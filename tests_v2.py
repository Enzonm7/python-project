from produit import Produit
from client import Client
from commande import Commande
from cafeteria import Cafeteria


# --- Tests Phase 1 : Annulation de commande ---
cafet = Cafeteria("Cafétéria Phase 1")
cafe = Produit("B01", "Café expresso", "boisson chaude", 1.20, 10)
wrap = Produit("W01", "Wrap végétarien", "plat", 4.60, 9)
cafet.ajouter_produit(cafe)
cafet.ajouter_produit(wrap)

chloe = Client("Chloé", "étudiant", 14.40)
cafet.inscrire_client(chloe)

visiteur = Client("Paul", "visiteur")
cafet.inscrire_client(visiteur)

# Une commande initiale acceptée pour que Chloé ait déjà 4 points issus de son historique
cmd_base = Commande(chloe, "12:00")
cmd_base.ajouter_ligne(wrap, 1)  # 4.60 € -> 4 points, stock wrap = 8, solde = 9.80 €
assert cafet.traiter_commande(cmd_base) == (True, "acceptée", 4.60)
assert chloe.points_fidelite == 4

# 1. Dernière commande annulée -> retour exact à l'état d'avant (solde, stock, fidélité)
solde_avant = chloe.solde
points_avant = chloe.points_fidelite
stock_wrap_avant = wrap.stock

cmd_chloe = Commande(chloe, "12:18")
cmd_chloe.ajouter_ligne(wrap, 1)  # 4.60 € -> solde = 5.20 €, points = 8, stock wrap = 7
assert cafet.traiter_commande(cmd_chloe) == (True, "acceptée", 4.60)
assert round(chloe.solde, 2) == 5.20
assert chloe.points_fidelite == 8
assert wrap.stock == 7

assert cafet.annuler_commande(cmd_chloe.numero) == (True, "annulée", 4.60)
assert round(chloe.solde, 2) == round(solde_avant, 2)
assert chloe.points_fidelite == points_avant
assert wrap.stock == stock_wrap_avant
assert cmd_chloe.statut == "annulée"

# 2 & 4. Annulation d'une commande inconnue -> refusée, rien n'est modifié
assert cafet.annuler_commande(999) == (False, "commande inconnue", 0.0)
assert cafet.refus["commande inconnue"] == 1
assert round(chloe.solde, 2) == round(solde_avant, 2)
assert wrap.stock == stock_wrap_avant
assert chloe.points_fidelite == points_avant

# 3 & 4. Annulation d'une commande déjà annulée -> refusée, rien n'est modifié
assert cafet.annuler_commande(cmd_chloe.numero) == (False, "commande déjà annulée", 0.0)
assert cafet.refus["commande déjà annulée"] == 1
assert round(chloe.solde, 2) == round(solde_avant, 2)
assert wrap.stock == stock_wrap_avant
assert chloe.points_fidelite == points_avant

# 5. Remboursement d'un visiteur (pas de solde de badge à modifier)
cmd_vis = Commande(visiteur, "10:00")
cmd_vis.ajouter_ligne(cafe, 2)  # 2.40 € comptant
assert cafet.traiter_commande(cmd_vis) == (True, "acceptée", 2.40)
assert cafet.annuler_commande(cmd_vis.numero) == (True, "annulée", 2.40)
assert visiteur.solde == 0.0
assert visiteur.points_fidelite == 0

# 6. Remboursement faisant dépasser 150,00 € (plafond de recharge non appliqué)
alice_p1 = Client("Alice", "étudiant", 149.00)
cafet.inscrire_client(alice_p1)
cmd_a = Commande(alice_p1, "10:00")
cmd_a.ajouter_ligne(cafe, 3)  # 3.60 € -> solde = 145.40 €
assert cafet.traiter_commande(cmd_a) == (True, "acceptée", 3.60)
alice_p1.solde = 149.00
assert cafet.annuler_commande(cmd_a.numero) == (True, "annulée", 3.60)
assert round(alice_p1.solde, 2) == 152.60

# 7. Annulation d'une commande ayant utilisé un avantage de fidélité
alice_p1.points_fidelite = 30
cmd_bon = Commande(alice_p1, "12:00")
cmd_bon.ajouter_ligne(wrap, 1)  # 4.60 € - 2.00 € (bon) = 2.60 € -> 30 - 30 + 2 = 2 points
assert cafet.traiter_commande(cmd_bon) == (True, "acceptée", 2.60)
assert alice_p1.points_fidelite == 2
assert cafet.annuler_commande(cmd_bon.numero) == (True, "annulée", 2.60)
assert alice_p1.points_fidelite == 0

# 8. Ticket d'une commande annulée
assert "ANNULÉE" in str(cmd_chloe)

print("Tous les tests de la Phase 1 v2.0 sont validés !")

# --- Tests Phase 2 : Rappel d'un produit ---
cafet_p2 = Cafeteria("Cafétéria Phase 2")
cafe_p2 = Produit("B01", "Café expresso", "boisson chaude", 1.20, 10)
wrap_p2 = Produit("W01", "Wrap végétarien", "plat", 4.60, 10)
jus_p2 = Produit("J01", "Jus d'orange", "boisson froide", 2.00, 8)
cafet_p2.ajouter_produit(cafe_p2)
cafet_p2.ajouter_produit(wrap_p2)
cafet_p2.ajouter_produit(jus_p2)

bruno_p2 = Client("Bruno", "étudiant", 20.00)
chloe_p2 = Client("Chloé", "étudiant", 20.00)
cafet_p2.inscrire_client(bruno_p2)
cafet_p2.inscrire_client(chloe_p2)

# Commande 1 de Bruno à 12:15 : 2 wraps = 9.20 € -> solde 10.80 €, 9 points, stock wrap = 8
cmd_b1 = Commande(bruno_p2, "12:15")
cmd_b1.ajouter_ligne(wrap_p2, 2)
assert cafet_p2.traiter_commande(cmd_b1) == (True, "acceptée", 9.20)

# Commande 2 de Chloé à 12:18 : 1 wrap = 4.60 € -> solde 15.40 €, 4 points, stock wrap = 7
cmd_c1 = Commande(chloe_p2, "12:18")
cmd_c1.ajouter_ligne(wrap_p2, 1)
assert cafet_p2.traiter_commande(cmd_c1) == (True, "acceptée", 4.60)

# 1. Rappel d'un produit présent dans plusieurs commandes (dans l'ordre chronologique)
res_rappel = cafet_p2.rappeler_produit("W01")
assert res_rappel["rappel"] is True
assert wrap_p2.rappel is True
assert wrap_p2.stock == 0
assert res_rappel["commandes_annulees"] == [cmd_b1.numero, cmd_c1.numero]
assert round(res_rappel["total_rembourse"], 2) == 13.80
assert round(bruno_p2.solde, 2) == 20.00
assert bruno_p2.points_fidelite == 0
assert round(chloe_p2.solde, 2) == 20.00
assert chloe_p2.points_fidelite == 0

# 2. Rappel d'un produit sans aucune commande (0 annulation)
res_jus = cafet_p2.rappeler_produit("J01")
assert res_jus["rappel"] is True
assert jus_p2.rappel is True
assert jus_p2.stock == 0
assert res_jus["commandes_annulees"] == []
assert res_jus["total_rembourse"] == 0.0

# 3. Commande contenant un produit rappelé : refusée, rien modifié
solde_bruno_avant = bruno_p2.solde
pts_bruno_avant = bruno_p2.points_fidelite
cmd_rappel = Commande(bruno_p2, "12:35")
cmd_rappel.ajouter_ligne(wrap_p2, 1)
assert cafet_p2.traiter_commande(cmd_rappel) == (False, "produit rappelé", 0.0)
assert cafet_p2.refus["produit rappelé"] == 1
assert wrap_p2.stock == 0
assert round(bruno_p2.solde, 2) == round(solde_bruno_avant, 2)
assert bruno_p2.points_fidelite == pts_bruno_avant

# 4. Réapprovisionnement d'un produit rappelé : refusé
assert not cafet_p2.reapprovisionner("W01", 10)
assert cafet_p2.refus["produit rappelé"] == 2
assert wrap_p2.stock == 0

# 5. Second rappel du même produit
res_second_rappel = cafet_p2.rappeler_produit("W01")
assert res_second_rappel["rappel"] is False
assert res_second_rappel["motif"] == "déjà rappelé"
assert cafet_p2.refus["déjà rappelé"] == 1
assert res_second_rappel["commandes_annulees"] == []
assert res_second_rappel["total_rembourse"] == 0.0

print("Tous les tests de la Phase 2 v2.0 sont validés !")