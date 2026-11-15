class Cafeteria:

    def __init__(self, nom="CampusCafé"):
        self.nom = nom
        self.catalogue = {}
        self.clients = {}
        self.commandes = []
        self.chiffre_affaires = 0.0
        self.total_remises = 0.0
        self.refus = {
            "produit inconnu": 0,
            "quantité invalide": 0,
            "rupture de stock": 0,
            "hors créneau": 0,
            "solde insuffisant": 0
        }

    def __repr__(self):
        return f"Cafetaria('{self.nom}', produit={len(self.catalogue)}, clients={len(self.clients)})"

    def ajouter_produit(self, produit):
        self.catalogue[produit.code] = produit

    def inscrire_client(self, client):
        self.clients[client.nom] = client

    def recharger_badge(self, nom_client, montant):
        if nom_client not in self.clients:
            return (False, "client inconnu")
        client = self.clients[nom_client]
        if client.recharger(montant):
            return (True, "recharge acceptée")
        return (False, "recharge refusée")

    def reapprovisionner(self, code_produit, quantite):
        if code_produit not in self.catalogue or quantite <= 0:
            return False
        self.catalogue[code_produit].reapprovisionner(quantite)
        return True

    def valider_commande(self, commande):
        if len(commande) <= 0:
            self.refus["quantité invalide"] += 1
            return (False, "quantité invalide", 0.0)
        total_brut = 0.0
        for produit, quantite in commande.lignes.items():
            if produit.code not in self.catalogue:
                self.refus["produit inconnu"] += 1
                return (False, "produit inconnu", 0.0)
            if produit.categorie == "plat" and not ("11:30" <= commande.heure < "14:00"):
                self.refus["hors créneau"] += 1
                return (False, "hors créneau", 0.0)
            if produit.stock < quantite:
                self.refus["rupture de stock"] += 1
                return (False, "rupture de stock", 0.0)
            total_brut += produit.prix * quantite
        total = commande.calculer_total()
        if not commande.client.peut_payer(total):
            self.refus["solde insuffisant"] += 1
            return (False, "solde insuffisant", 0.0)
        for produit, quantite in commande.lignes.items():
            produit.se_vendre(quantite)
        if commande.client.profil != "visiteur":
            commande.client.etre_debite(total)
        commande.client.calculer_avantage_fidelite(total)
        remise = round(total_brut - total, 2)
        self.chiffre_affaires = round(self.chiffre_affaires + total, 2)
        self.total_remises = round(self.total_remises + remise, 2)
        self.commandes.append(commande)
        return (True, "acceptée", total)

    def afficher_rapport(self):
        print(f"\n=== RAPPORT DE CLÔTURE : {self.nom} ===")
        print(f"Chiffre d'affaires total : {self.chiffre_affaires:.2f} €")
        print(f"Nombre de commandes validées : {len(self.commandes)}")
        for motif, nb in self.refus.items():
            print(f"- {motif} : {nb}")
        print(f"\nChiffre d'affaires total : {self.chiffre_affaires:.2f} €")
        print(f"Total des remises et avantages accordés : {self.total_remises:.2f} €")

        ventes = {}
        for cmd in self.commandes:
            for produit, quantite in cmd.lignes.items():
                if produit.nom in ventes:
                    ventes[produit.nom] += quantite
                else:
                    ventes[produit.nom] = quantite
        liste_ventes = []
        for nom_produit, quantite in ventes.items():
            liste_ventes.append((quantite, nom_produit))
        top3 = sorted(liste_ventes, reverse=True)[:3]
        print("\nTop 3 des produits les plus vendus :")
        for quantite, nom_produit in top3:
            print(f"- {nom_produit} : {quantite} vendu(s)")

        print("\nCarte triée par prix croissant :")
        for produit in sorted(self.catalogue.values()):
            mention = "[Epuisé]" if produit.stock == 0 else ""
            print(f"- {produit.nom} ({produit.code}) : {produit.prix:.2f} € | Stock : {produit.stock}{mention}")

        print("\nBadges avec solde inférieur à 3,00 € :")
        for client in self.clients.values():
            if client.profil != "visiteur" and client.solde < 3.00:
                print(f"- {client.nom} ({client.profil}) : {client.solde:.2f} €")