from produit import Produit
from client import Client
from commande import Commande
from cafeteria import Cafeteria


def traiter_commande(cafet, num_evt, commande):
    acceptee, motif, montant = cafet.traiter_commande(commande)
    if acceptee:
        print(f"[Evt {num_evt} - {commande.heure}] OK | Commande n°{commande.numero} ({commande.client.nom}) : {montant:.2f} €")
        print(commande)
    else:
        print(f"[Evt {num_evt} - {commande.heure}] REFUS ({motif}) | Commande n°{commande.numero} ({commande.client.nom})")
    print()


def traiter_recharge(cafet, num_evt, heure, nom_client, montant):
    acceptee, motif = cafet.recharger_badge(nom_client, montant)
    statut = "OK" if acceptee else "REFUS"
    print(f"[Evt {num_evt} - {heure}] Recharge {nom_client} ({montant:.2f} €) : {statut} ({motif})\n")


def traiter_reappro(cafet, num_evt, heure, code_produit, quantite):
    if cafet.reapprovisionner(code_produit, quantite):
        print(f"[Evt {num_evt} - {heure}] Réapprovisionnement {code_produit} (+{quantite}) : OK\n")


# 1. Initialisation de la cafétéria (Evénement 1 : 07:30 Ouverture)
cafet = Cafeteria("CampusCafé")
print("[Evt 1 - 07:30] Ouverture de la cafétéria\n")

# 2. Création de la carte officielle (11 produits)
b01 = Produit("B01", "Café expresso", "boisson chaude", 1.20, 100)
b02 = Produit("B02", "Thé", "boisson chaude", 1.30, 60)
b03 = Produit("B03", "Chocolat chaud", "boisson chaude", 1.60, 40)
b04 = Produit("B04", "Jus d'orange", "boisson froide", 2.00, 24)
b05 = Produit("B05", "Eau 50 cl", "boisson froide", 1.00, 40)
v01 = Produit("V01", "Croissant", "viennoiserie", 1.20, 30)
p01 = Produit("P01", "Sandwich jambon-beurre", "plat", 4.00, 15)
p02 = Produit("P02", "Wrap végétarien", "plat", 4.60, 10)
p03 = Produit("P03", "Plat du jour", "plat", 7.20, 20)
d01 = Produit("D01", "Cookie", "dessert", 1.40, 25)
d02 = Produit("D02", "Fruit de saison", "dessert", 0.80, 30)

for produit in [b01, b02, b03, b04, b05, v01, p01, p02, p03, d01, d02]:
    cafet.ajouter_produit(produit)

# Produit hors carte utilisé uniquement pour tester l'événement 13 ("produit inconnu")
smoothie_inconnu = Produit("S01", "Smoothie mangue", "boisson froide", 3.00, 10)

# 3. Inscription des clients titulaires d'un badge (+ objet visiteur non inscrit)
alice = Client("Alice", "étudiant", 12.00)
bruno = Client("Bruno", "alternant", 3.50)
chloe = Client("Chloé", "étudiant", 25.00)
farid = Client("Farid", "personnel", 0.00)
visiteur = Client("Visiteur", "visiteur", 0.00)

for client in [alice, bruno, chloe, farid]:
    cafet.inscrire_client(client)

# 4. Déroulement chronologique des événements 2 à 16
# Evt 2 - 07:45 : Alice (Café expresso, Croissant)
cmd2 = Commande(alice, "07:45")
cmd2.ajouter_ligne(b01, 1)
cmd2.ajouter_ligne(v01, 1)
traiter_commande(cafet, 2, cmd2)

# Evt 3 - 08:10 : Farid (Café expresso x 2)
cmd3 = Commande(farid, "08:10")
cmd3.ajouter_ligne(b01, 2)
traiter_commande(cafet, 3, cmd3)

# Evt 4 - 08:30 : Bruno (Chocolat chaud, Croissant x 3)
cmd4 = Commande(bruno, "08:30")
cmd4.ajouter_ligne(b03, 1)
cmd4.ajouter_ligne(v01, 3)
traiter_commande(cafet, 4, cmd4)

# Evt 5 - 08:35 : Recharge Bruno (20,00 €)
traiter_recharge(cafet, 5, "08:35", "Bruno", 20.00)

# Evt 6 - 08:40 : Bruno (Chocolat chaud, Croissant x 3)
cmd6 = Commande(bruno, "08:40")
cmd6.ajouter_ligne(b03, 1)
cmd6.ajouter_ligne(v01, 3)
traiter_commande(cafet, 6, cmd6)

# Evt 7 - 09:15 : Visiteur (Thé, Cookie)
cmd7 = Commande(visiteur, "09:15")
cmd7.ajouter_ligne(b02, 1)
cmd7.ajouter_ligne(d01, 1)
traiter_commande(cafet, 7, cmd7)

# Evt 8 - 11:00 : Chloé (Plat du jour -> hors créneau)
cmd8 = Commande(chloe, "11:00")
cmd8.ajouter_ligne(p03, 1)
traiter_commande(cafet, 8, cmd8)

# Evt 9 - 12:05 : Chloé (Plat du jour, Jus d'orange, Cookie)
cmd9 = Commande(chloe, "12:05")
cmd9.ajouter_ligne(p03, 1)
cmd9.ajouter_ligne(b04, 1)
cmd9.ajouter_ligne(d01, 1)
traiter_commande(cafet, 9, cmd9)

# Evt 10 - 12:10 : Recharge Alice (150,00 € -> refusée car > 100,00 €)
traiter_recharge(cafet, 10, "12:10", "Alice", 150.00)

# Evt 11 - 12:20 : Alice (Wrap végétarien, Eau 50 cl, Fruit de saison, Café expresso)
cmd11 = Commande(alice, "12:20")
cmd11.ajouter_ligne(p02, 1)
cmd11.ajouter_ligne(b05, 1)
cmd11.ajouter_ligne(d02, 1)
cmd11.ajouter_ligne(b01, 1)
traiter_commande(cafet, 11, cmd11)

# Evt 12 - 12:45 : Visiteur (Sandwich jambon-beurre x 16 -> rupture de stock)
cmd12 = Commande(visiteur, "12:45")
cmd12.ajouter_ligne(p01, 16)
traiter_commande(cafet, 12, cmd12)

# Evt 13 - 13:00 : Bruno (Sandwich jambon-beurre, Smoothie mangue -> produit inconnu)
cmd13 = Commande(bruno, "13:00")
cmd13.ajouter_ligne(p01, 1)
cmd13.ajouter_ligne(smoothie_inconnu, 1)
traiter_commande(cafet, 13, cmd13)

# Evt 14 - 15:30 : Alice (Café expresso, Cookie -> Happy Hour sur la boisson)
cmd14 = Commande(alice, "15:30")
cmd14.ajouter_ligne(b01, 1)
cmd14.ajouter_ligne(d01, 1)
traiter_commande(cafet, 14, cmd14)

# Evt 15 - 16:00 : Réapprovisionnement (Sandwich jambon-beurre + 10)
traiter_reappro(cafet, 15, "16:00", "P01", 10)

# Evt 16 - 17:30 : Farid (Thé x 2 -> hors Happy Hour, mais -5% personnel)
cmd16 = Commande(farid, "17:30")
cmd16.ajouter_ligne(b02, 2)
traiter_commande(cafet, 16, cmd16)

# 5. Clôture de la journée (Evénement 17 : 18:30)
print("[Evt 17 - 18:30] Clôture de la journée")
cafet.afficher_rapport()