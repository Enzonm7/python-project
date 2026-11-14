class Commande:

    COMPTEUR_NUMERO = 1

    def __init__(self, client, heure):
        self.numero = Commande.COMPTEUR_NUMERO
        Commande.COMPTEUR_NUMERO += 1
        self.client = client
        self.heure = heure
        self.lignes = {}

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

    def calculer_total(self):
        total = 0.0
        for produit, quantite in self.lignes.items():
            sous_total = produit.prix * quantite
            if produit.categorie in ["boisson chaude", "boisson froide"] and "15:00" <= self.heure < "17:00" and self.client.profil != "visiteur":
                sous_total *= 0.80
            total += sous_total
        if self.client.profil == "personnel":
            total *= 0.95
        if self.client.profil != "visiteur" and self.client.points_fidelite >= 30:
            total -= 2.00
        return round(max(0.0, total), 2)

    def __str__(self):
        ticket = f"=== Commande n°{self.numero} ===\n"
        ticket += f"Client : {self.client.nom} ({self.client.profil})\n"
        ticket += f"Heure : {self.heure}\n"
        ticket += "-------------------------\n"
        for produit, quantite in self.lignes.items():
            prix_ligne = produit.prix * quantite
            ticket += f"{quantite}x {produit.nom} : {prix_ligne:.2f} €\n"
        ticket += "-------------------------\n"
        ticket += f"TOTAL À PAYER : {self.calculer_total():.2f} €"
        return ticket