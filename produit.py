class Produit:

    CATEGORIE_RESTREINTE = "plat"
    HEURE_DEBUT_SERVICE = "11:30"
    HEURE_FIN_SERVICE = "14:00"

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
        if not isinstance(autre, Produit):
            return NotImplemented
        return self.code == autre.code

    def __hash__(self):
        return hash(self.code)

    def __lt__(self, autre):
        if not isinstance(autre, Produit):
            return NotImplemented
        return self.prix < autre.prix

    def se_vendre(self, quantite):
        self.stock -= quantite

    def reapprovisionner(self, quantite):
        self.stock += quantite

    def a_assez_de_stock(self, quantite):
        return self.stock >= quantite

    def est_dans_creneau(self, heure):
        if self.categorie == Produit.CATEGORIE_RESTREINTE:
            return Produit.HEURE_DEBUT_SERVICE <= heure < Produit.HEURE_FIN_SERVICE
        return True

    def est_disponible(self, quantite, heure):
        return self.a_assez_de_stock(quantite) and self.est_dans_creneau(heure)