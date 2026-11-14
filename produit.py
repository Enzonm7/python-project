class Produit:

    def __init__(self, code, nom, categorie, prix, stock):
        self.code = code
        self.nom = nom
        self.categorie = categorie
        self.prix = prix
        self.stock = stock

    def __str__(self):
        return f"Code produit: {self.code}, Nom: {self.nom}, Catégorie: {self.categorie}, Prix: {self.prix:.2f} €"

    def __repr__(self):
        return f"Produit('{self.code}', '{self.nom}', '{self.categorie}', {self.prix}, {self.stock})"

    def __eq__(self, autre):
        return self.code == autre.code

    def __hash__(self):
        return hash(self.code)

    def __lt__(self, autre):
        return self.prix < autre.prix

    def se_vendre(self, quantite):
        self.stock -= quantite

    def reapprovisionner(self, quantite):
        self.stock += quantite

    def est_disponible(self, quantite, heure):
        if self.stock < quantite:
            return False
        if self.categorie == 'plat' and not ("11:30" <= heure < "14:00"):
            return False
        return True