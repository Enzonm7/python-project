class Cafeteria:
    """Gère la carte des produits, les clients inscrits, le traitement des commandes et le bilan financier."""

    SEUIL_ALERTE_SOLDE = 3.00

    def __init__(self, nom="CampusCafé"):
        """Initialise la cafétéria avec son catalogue, ses clients, sa caisse et ses compteurs de refus."""
        self.nom = nom
        self.catalogue = {}
        self.clients = {}
        self.commandes = []
        self.historique_refus = []
        self.historique_rappels = []
        self.chiffre_affaires = 0.0
        self.total_remises = 0.0
        self.total_rembourse = 0.0
        self.refus = {
            "produit inconnu": 0,
            "quantité invalide": 0,
            "rupture de stock": 0,
            "hors créneau": 0,
            "solde insuffisant": 0,
            "commande inconnue": 0,
            "commande déjà annulée": 0,
            "produit rappelé": 0,
            "déjà rappelé": 0
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
        produit = self.catalogue[code_produit]
        if produit.rappel:
            self.refus["produit rappelé"] += 1
            return False
        produit.reapprovisionner(quantite)
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
            if produit_carte.rappel:
                return "produit rappelé"
            if not produit_carte.est_dans_creneau(commande.heure):
                return "hors créneau"
            if not produit_carte.a_assez_de_stock(quantite):
                return "rupture de stock"

        return None

    def refuser_commande(self, motif, client=None):
        """Incrémente le compteur du motif de refus et renvoie le triplet d'échec."""
        self.refus[motif] += 1
        if client is not None:
            self.historique_refus.append((client.nom, motif))
        return (False, motif, 0.0)

    def creer_resume_rappel(self, rappel, motif):
        """Construit un résumé standardisé du résultat d'un rappel de produit."""
        return {
            "rappel": rappel,
            "motif": motif,
            "commandes_annulees": [],
            "clients_rembourses": {},
            "total_rembourse": 0.0,
        }

    def rappeler_produit(self, code_produit):
        """Rappelle un produit, détruit son stock et annule les commandes concernées dans l'ordre chronologique."""
        if code_produit not in self.catalogue:
            return self.creer_resume_rappel(False, "produit inconnu")

        produit = self.catalogue[code_produit]
        if produit.rappel:
            self.refus["déjà rappelé"] += 1
            return self.creer_resume_rappel(False, "déjà rappelé")

        produit.rappel = True
        produit.stock = 0

        resume = self.creer_resume_rappel(True, "produit rappelé")

        for cmd in self.commandes:
            if cmd.statut != "annulée" and produit in cmd:
                cmd.annulee_par_rappel = True
                ok, message, montant = self.annuler_commande(cmd.numero)
                if ok:
                    resume["commandes_annulees"].append(cmd.numero)
                    nom_client = cmd.client.nom
                    remb_client = resume["clients_rembourses"].get(nom_client, 0.0)
                    resume["clients_rembourses"][nom_client] = round(remb_client + montant, 2)
                    resume["total_rembourse"] = round(resume["total_rembourse"] + montant, 2)

        return resume

    def traiter_commande(self, commande):
        """Vérifie, encaisse et enregistre une commande en garantissant qu'aucune donnée ne change en cas de refus."""
        # 1. Vérifier
        motif_refus = self.verifier_commande(commande)
        if motif_refus is not None:
            return self.refuser_commande(motif_refus, commande.client)

        # 2. Calculer les totaux
        total_brut = commande.calculer_total_brut()
        total = commande.calculer_total()

        # 3. Encaisser
        if not commande.client.peut_payer(total):
            return self.refuser_commande("solde insuffisant", commande.client)
        commande.client.etre_debite(total)
        commande.montant_paye = total
        commande.client.commandes.append(commande)

        # 4. Enregistrer
        for produit, quantite in commande:
            self.catalogue[produit.code].se_vendre(quantite)

        commande.client.actualiser_fidelite(total)

        remise = round(total_brut - total, 2)
        self.chiffre_affaires = round(self.chiffre_affaires + total, 2)
        self.total_remises = round(self.total_remises + remise, 2)
        self.commandes.append(commande)

        return (True, "acceptée", total)

    def annuler_commande(self, numero_commande):
        commande_cible = None
        for cmd in self.commandes:
            if cmd.numero == numero_commande:
                commande_cible = cmd
                break
        if commande_cible is None:
            self.refuser_commande("commande inconnue")
            return(False, "commande inconnue", 0.0)

        if commande_cible.statut == "annulée":
            self.refuser_commande("commande déjà annulée", commande_cible.client)
            return(False, "commande déjà annulée", 0.0)

        commande_cible.statut = "annulée"

        # 1. Remise en stock sur le catalogue si le produit n'est pas rappelé
        for produit, quantite in commande_cible:
            produit_carte = self.catalogue[produit.code]
            if not produit_carte.rappel:
                produit_carte.stock += quantite

        # 2. Remboursement du badge (ou comptant pour un visiteur)
        montant_rembourse = round(commande_cible.montant_paye or 0.0, 2)
        client = commande_cible.client
        if client.a_un_badge():
            client.solde = round(client.solde + montant_rembourse, 2)

        # 3. Recalcul de la fidélité en rejouant les commandes valides restantes
        client.rejouer_fidelite(client.commandes)
        self.total_rembourse = round(self.total_rembourse + montant_rembourse, 2)

        return(True, "annulée", montant_rembourse)


    def afficher_rapport(self):
        """Affiche le bilan de clôture de crise : ventes non annulées, annulations, rappels, carte et soldes."""
        nb_commandes_validees = 0
        nb_commandes_annulees = 0
        nb_annulees_rappel = 0
        for cmd in self.commandes:
            if cmd.statut == "annulée":
                nb_commandes_annulees += 1
                if cmd.annulee_par_rappel:
                    nb_annulees_rappel += 1
            else:
                nb_commandes_validees += 1

        print(f"\n=== RAPPORT DE CLÔTURE : {self.nom} ===")
        print(f"Chiffre d'affaires total : {self.chiffre_affaires:.2f} €")
        print(f"Total remboursé : {self.total_rembourse:.2f} €")
        print(f"Nombre de commandes validées : {nb_commandes_validees}")
        print(f"Nombre de commandes annulées : {nb_commandes_annulees} (dont {nb_annulees_rappel} dues au rappel)")
        print(f"Total des remises et avantages accordés : {self.total_remises:.2f} €")

        print("\nDétail des refus :")
        for motif, nb in self.refus.items():
            print(f"- {motif} : {nb}")
        print("\nClients ayant eu des refus :")
        if not self.historique_refus:
            print("Aucun refus enregistré")
        else:
            for nom_client, motif in self.historique_refus:
                print(f"{nom_client} : {motif}")
            print(f"Nombre de refus enregistré : {len(self.historique_refus)}")

        ventes = {}
        for cmd in self.commandes:
            if cmd.statut != "annulée":
                for produit, quantite in cmd:
                    ventes[produit.nom] = ventes.get(produit.nom, 0) + quantite

        liste_ventes = []
        for nom_produit, quantite in ventes.items():
            liste_ventes.append((quantite, nom_produit))
        top3 = sorted(liste_ventes, reverse=True)[:3]

        print("\nTop 3 des produits les plus vendus :")
        for quantite, nom_produit in top3:
            print(f"- {nom_produit} : {quantite} vendu(s)")

        print("\nDétail des rappels de produits :")
        if not self.historique_rappels:
            print("- Aucun rappel de produit")
        else:
            for rappel in self.historique_rappels:
                code_prod = rappel["code_produit"]
                print(f"- Produit rappelé ({code_prod}) | Total remboursé : {rappel['total_rembourse']:.2f} €")
                liste_clients = []
                for nom_client, montant in rappel["clients_rembourses"].items():
                    liste_clients.append((montant, nom_client))
                for montant, nom_client in sorted(liste_clients, reverse=True):
                    print(f"  * {nom_client} : {montant:.2f} €")

        print("\nCarte triée par prix croissant :")
        for produit in sorted(self.catalogue.values()):
            if produit.rappel:
                mention = " [Rappelé]"
            elif produit.stock == 0:
                mention = " [Epuisé]"
            else:
                mention = ""
            print(f"- {produit.nom} ({produit.code}) : {produit.prix:.2f} € | Stock : {produit.stock}{mention}")

        print("\nSolde des badges en fin de journée :")
        for client in self.clients.values():
            print(f"- {client.nom} ({client.profil}) :\n Solde : {client.solde:.2f} €, Points fidélité : {client.points_fidelite}")

        print(f"\nBadges avec solde inférieur à {Cafeteria.SEUIL_ALERTE_SOLDE:.2f} € :")
        for client in self.clients.values():
            if client.solde < Cafeteria.SEUIL_ALERTE_SOLDE:
                print(f"- {client.nom} ({client.profil}) :\n Solde : {client.solde:.2f} €")