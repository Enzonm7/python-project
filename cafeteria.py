class Cafeteria:

    def __init__(self, nom):
        self.nom = nom
        self.catalogue = {}
        self.clients = {}
        self.commandes = []
        self.chiffre_affaires = 0.0

    def ajouter_produit(self, produit):
        self.catalogue[produit.code] = produit

    def inscrire_client(self, client):
        self.clients[client.nom] = client

    def valider_commande(self, commande):
        if len(commande) == 0:
            return False
        for produit, quantite in commande.lignes.items():
            if not produit.est_disponible(quantite, commande.heure):
                return False
        total = commande.calculer_total()
        if not commande.client.peut_payer(total):
            return False
        for produit, quantite in commande.lignes.items():
            produit.se_vendre(quantite)
        if commande.client.profil != "visiteur":
            commande.client.etre_debite(total)
        commande.client.calculer_avantage_fidelite(total)
        self.chiffre_affaires = round(self.chiffre_affaires + total, 2)
        self.commandes.append(commande)
        return True

    def afficher_rapport(self):
        print(f"\n=== RAPPORT DE CLÔTURE : {self.nom} ===")
        print(f"Chiffre d'affaires total : {self.chiffre_affaires:.2f} €")
        print(f"Nombre de commandes validées : {len(self.commandes)}")

        print("\n--- Catalogue et stocks (triés par prix croissant) ---")
        for produit in sorted(self.catalogue.values()):
            print(f"- {produit.nom} ({produit.code}) : {produit.prix:.2f} € | Stock restant : {produit.stock}")

        print("\n--- Soldes et fidélité clients ---")
        for client in self.clients.values():
            print(f"- {client.nom} ({client.profil}) : Solde = {client.solde:.2f} € | Points = {client.points_fidelite}")