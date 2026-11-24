from client import Client


class Commande:
    """Représente une commande passée par un client à une heure donnée et calcule son montant avec remises."""

    COMPTEUR_NUMERO = 1
    CATEGORIES_HAPPY_HOUR = ["boisson chaude", "boisson froide"]
    DEBUT_HAPPY_HOUR = "15:00"
    FIN_HAPPY_HOUR = "17:00"
    HAPPY_HOUR = 0.80
    REMISE_PERSONNEL = 0.95

    def __init__(self, client, heure):
        """Crée une nouvelle commande numérotée automatiquement pour un client et un horaire donnés."""
        self.numero = Commande.COMPTEUR_NUMERO
        Commande.COMPTEUR_NUMERO += 1
        self.client = client
        self.heure = heure
        self.lignes = {}
        self.statut = "acceptée"
        self.montant_paye = None
        self.annulee_par_rappel = False
        self.remise_appliquee = 0.0

    def __repr__(self):
        """Renvoie la représentation technique de la commande."""
        return f"Commande({repr(self.client)}, '{self.heure}')"

    def ajouter_ligne(self, produit, quantite):
        """Ajoute un produit à la commande ou cumule sa quantité s'il est déjà présent."""
        if produit in self.lignes:
            self.lignes[produit] += quantite
        else:
            self.lignes[produit] = quantite

    def __len__(self):
        """Renvoie le nombre total d'articles dans la commande."""
        return sum(self.lignes.values())

    def __contains__(self, produit):
        """Permet de tester avec 'in' si un produit figure dans la commande."""
        return produit in self.lignes

    def __iter__(self):
        """Permet de parcourir directement les couples (produit, quantite) de la commande."""
        return iter(self.lignes.items())

    def calculer_total_brut(self):
        """Calcule le montant total de la commande avant toute remise."""
        total = 0.0
        for produit, quantite in self.lignes.items():
            total += produit.prix * quantite
        return round(total, 2)

    def calculer_total(self):
        """Calcule le montant final à payer : Happy Hour (-20 %) sur les boissons avec badge, remise personnel (-5 %), puis bon fidélité (-2 €)."""
        total = 0.0
        est_happy_hour = Commande.DEBUT_HAPPY_HOUR <= self.heure < Commande.FIN_HAPPY_HOUR
        a_badge = self.client.a_un_badge()

        for produit, quantite in self.lignes.items():
            sous_total = produit.prix * quantite
            est_boisson = produit.categorie in Commande.CATEGORIES_HAPPY_HOUR
            if est_boisson and est_happy_hour and a_badge:
                sous_total *= Commande.HAPPY_HOUR
            total += sous_total

        if self.client.profil == "personnel":
            total *= Commande.REMISE_PERSONNEL

        if self.client.a_droit_au_bon():
            total -= Client.MONTANT_BON_FIDELITE

        return round(max(0.0, total), 2)

    def __str__(self):
        """Génère le ticket de caisse en affichant le montant réellement encaissé (ou estimé si la commande n'est pas encore payée)."""
        montant_affiche = self.montant_paye if self.montant_paye is not None else self.calculer_total()
        entete = f"=== Commande n°{self.numero} [ANNULÉE] ===" if self.statut == "annulée" else f"=== Commande n°{self.numero} ==="
        ticket = f"{entete}\n"
        ticket += f"Client : {self.client.nom} ({self.client.profil})\n"
        ticket += f"Heure : {self.heure}\n"
        ticket += "-------------------------\n"
        for produit, quantite in self.lignes.items():
            prix_ligne = produit.prix * quantite
            ticket += f"{quantite}x {produit.nom} : {prix_ligne:.2f} €\n"
        ticket += "-------------------------\n"
        ticket += f"TOTAL À PAYER : {montant_affiche:.2f} €"
        return ticket