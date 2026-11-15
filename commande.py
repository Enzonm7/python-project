from client import Client

class Commande:

    COMPTEUR_NUMERO = 1
    CATEGORIES_HAPPY_HOUR = ["boisson chaude", "boisson froide"]
    DEBUT_HAPPY_HOUR = "15:00"
    FIN_HAPPY_HOUR = "17:00"
    HAPPY_HOUR = 0.80
    REMISE_PERSONNEL = 0.95

    def __init__(self, client, heure):
        self.numero = Commande.COMPTEUR_NUMERO
        Commande.COMPTEUR_NUMERO += 1
        self.client = client
        self.heure = heure
        self.lignes = {}
        self.montant_paye = None

    def __repr__(self):
        return f"Commande({repr(self.client)}, '{self.heure}')"

    def ajouter_ligne(self, produit, quantite):
        if produit in self.lignes:
            self.lignes[produit] += quantite
        else:
            self.lignes[produit] = quantite

    def __len__(self):
        return sum(self.lignes.values())

    def __contains__(self, produit):
        return produit in self.lignes

    def __iter__(self):
        return iter(self.lignes.items())

    def calculer_total_brut(self):
        total = 0.0
        for produit, quantite in self.lignes.items():
            total += produit.prix * quantite
        return round(total, 2)

    def calculer_total(self):
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
        montant_affiche = self.montant_paye if self.montant_paye is not None else self.calculer_total()

        ticket = f"=== Commande n°{self.numero} ===\n"
        ticket += f"Client : {self.client.nom} ({self.client.profil})\n"
        ticket += f"Heure : {self.heure}\n"
        ticket += "-------------------------\n"
        for produit, quantite in self.lignes.items():
            prix_ligne = produit.prix * quantite
            ticket += f"{quantite}x {produit.nom} : {prix_ligne:.2f} €\n"
        ticket += "-------------------------\n"
        ticket += f"TOTAL À PAYER : {montant_affiche:.2f} €"
        return ticket