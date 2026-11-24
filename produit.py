class Produit:
    """Représente un article de la carte de la cafétéria avec son prix, son stock et ses règles horaires."""

    CATEGORIE_RESTREINTE = "plat"
    HEURE_DEBUT_SERVICE = "11:30"
    HEURE_FIN_SERVICE = "14:00"

    def __init__(self, code, nom, categorie, prix, stock):
        """Initialise un produit avec son code unique, son nom, sa catégorie, son prix et son stock."""
        self.code = code
        self.nom = nom
        self.categorie = categorie
        self.prix = prix
        self.stock = stock
        self.rappel = False

    def __str__(self):
        """Renvoie une description lisible du produit pour l'affichage."""
        return f"Code produit: {self.code}, Nom: {self.nom}, Catégorie: {self.categorie}, Prix: {self.prix:.2f} €"

    def __repr__(self):
        """Renvoie la représentation technique permettant de recréer l'objet."""
        return f"Produit('{self.code}', '{self.nom}', '{self.categorie}', {self.prix}, {self.stock})"

    def __eq__(self, autre):
        """Vérifie si deux produits sont identiques en comparant leur code (renvoie NotImplemented si ce n'est pas un Produit)."""
        if not isinstance(autre, Produit):
            return NotImplemented
        return self.code == autre.code

    def __hash__(self):
        """Calcule l'empreinte du produit à partir de son code pour l'utiliser comme clé de dictionnaire."""
        return hash(self.code)

    def __lt__(self, autre):
        """Compare le prix de deux produits pour permettre le tri par prix croissant."""
        if not isinstance(autre, Produit):
            return NotImplemented
        return self.prix < autre.prix

    def se_vendre(self, quantite):
        """Diminue le stock du produit lors d'une vente."""
        if self.rappel:
            self.stock = 0
            return False
        self.stock -= quantite
        return True

    def reapprovisionner(self, quantite):
        """Augmente le stock du produit lors d'un réapprovisionnement."""
        if self.rappel:
            self.stock = 0
            return False
        self.stock += quantite
        return True

    def a_assez_de_stock(self, quantite):
        """Vérifie s'il reste suffisamment d'unités en stock pour honorer la demande."""
        return self.stock >= quantite

    def est_dans_creneau(self, heure):
        """Vérifie si le produit peut être commandé à l'heure donnée (les plats sont limités au service du midi)."""
        if self.categorie == Produit.CATEGORIE_RESTREINTE:
            return Produit.HEURE_DEBUT_SERVICE <= heure < Produit.HEURE_FIN_SERVICE
        return True

    def est_disponible(self, quantite, heure):
        """Vérifie à la fois que le stock est suffisant et que l'horaire est autorisé."""
        return self.a_assez_de_stock(quantite) and self.est_dans_creneau(heure)