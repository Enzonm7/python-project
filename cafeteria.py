class Cafeteria:
    """Gère la carte des produits, les clients inscrits, le traitement des commandes et le bilan financier."""

    SEUIL_ALERTE_SOLDE = 3.00

    def __init__(self, nom="CampusCafé"):
        """Initialise la cafétéria avec son catalogue, ses clients, sa caisse et ses compteurs de refus."""
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
        """Renvoie un résumé technique de l'état de la cafétéria."""
        return f"Cafeteria('{self.nom}', produits={len(self.catalogue)}, clients={len(self.clients)})"

    def ajouter_produit(self, produit):
        """Ajoute ou met à jour un produit dans le catalogue officiel."""
        self.catalogue[produit.code] = produit

    def inscrire_client(self, client):
        """Enregistre un client titulaire d'un badge dans la base de la cafétéria."""
        self.clients[client.nom] = client

    def recharger_badge(self, nom_client, montant):
        """Recherche le client par son nom et tente de recharger son badge."""
        if nom_client not in self.clients:
            return (False, "client inconnu")
        client = self.clients[nom_client]
        if client.recharger(montant):
            return (True, "recharge acceptée")
        return (False, "recharge refusée")

    def reapprovisionner(self, code_produit, quantite):
        """Ajoute du stock à un produit du catalogue si son code existe et que la quantité est positive."""
        if code_produit not in self.catalogue or quantite <= 0:
            return False
        self.catalogue[code_produit].reapprovisionner(quantite)
        return True

    def verifier_commande(self, commande):
        """Contrôle la validité d'une commande dans l'ordre : codes au catalogue, quantités positives, créneau et stock."""
        if len(commande.lignes) == 0:
            return "quantité invalide"

        # 1. Vérification des codes
        for produit, quantite in commande:
            if produit.code not in self.catalogue:
                return "produit inconnu"

        # 2. Vérification des quantités de chaque ligne
        for produit, quantite in commande:
            if quantite <= 0:
                return "quantité invalide"

        # 3. Vérification de la disponibilité (créneau puis stock sur la carte)
        for produit, quantite in commande:
            produit_carte = self.catalogue[produit.code]
            if not produit_carte.est_dans_creneau(commande.heure):
                return "hors créneau"
            if not produit_carte.a_assez_de_stock(quantite):
                return "rupture de stock"

        return None

    def refuser_commande(self, motif):
        """Incrémente le compteur du motif de refus et renvoie le triplet d'échec."""
        self.refus[motif] += 1
        return (False, motif, 0.0)

    def traiter_commande(self, commande):
        """Vérifie, encaisse et enregistre une commande en garantissant qu'aucune donnée ne change en cas de refus."""
        # 1. Vérifier
        motif_refus = self.verifier_commande(commande)
        if motif_refus is not None:
            return self.refuser_commande(motif_refus)

        # 2. Calculer les totaux
        total_brut = commande.calculer_total_brut()
        total = commande.calculer_total()

        # 3. Encaisser
        if not commande.client.peut_payer(total):
            return self.refuser_commande("solde insuffisant")
        commande.client.etre_debite(total)
        commande.montant_paye = total

        # 4. Enregistrer
        for produit, quantite in commande:
            self.catalogue[produit.code].se_vendre(quantite)

        commande.client.actualiser_fidelite(total)

        remise = round(total_brut - total, 2)
        self.chiffre_affaires = round(self.chiffre_affaires + total, 2)
        self.total_remises = round(self.total_remises + remise, 2)
        self.commandes.append(commande)

        return (True, "acceptée", total)

    def afficher_rapport(self):
        """Affiche le bilan de clôture : chiffre d'affaires, refus, top 3 des ventes, carte triée et alertes de solde."""
        print(f"\n=== RAPPORT DE CLÔTURE : {self.nom} ===")
        print(f"Chiffre d'affaires total : {self.chiffre_affaires:.2f} €")
        print(f"Nombre de commandes validées : {len(self.commandes)}")
        for motif, nb in self.refus.items():
            print(f"- {motif} : {nb}")
        print(f"Total des remises et avantages accordés : {self.total_remises:.2f} €")

        ventes = {}
        for cmd in self.commandes:
            for produit, quantite in cmd:
                ventes[produit.nom] = ventes.get(produit.nom, 0) + quantite

        liste_ventes = []
        for nom_produit, quantite in ventes.items():
            liste_ventes.append((quantite, nom_produit))
        top3 = sorted(liste_ventes, reverse=True)[:3]

        print("\nTop 3 des produits les plus vendus :")
        for quantite, nom_produit in top3:
            print(f"- {nom_produit} : {quantite} vendu(s)")

        print("\nCarte triée par prix croissant :")
        for produit in sorted(self.catalogue.values()):
            mention = " [Epuisé]" if produit.stock == 0 else ""
            print(f"- {produit.nom} ({produit.code}) : {produit.prix:.2f} € | Stock : {produit.stock}{mention}")

        print(f"\nSolde des badges en fin de journée :")
        for client in self.clients.values():
            print(f"- {client.nom} ({client.profil}) :\n Solde : {client.solde:.2f} €, Points fidélité : {client.points_fidelite}")

        print(f"\nBadges avec solde inférieur à {Cafeteria.SEUIL_ALERTE_SOLDE:.2f} € :")
        for client in self.clients.values():
            if client.solde < Cafeteria.SEUIL_ALERTE_SOLDE:
                print(f"- {client.nom} ({client.profil}) :\n Solde : {client.solde:.2f} €")