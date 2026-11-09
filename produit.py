class Produit:

    def __init__(self, code, nom, categorie, prix, stock):
        self.code = code
        self.nom = nom
        self.categorie = categorie
        self.prix = prix
        self.stock = stock

    def __str__(self):
        return f"Code produit: {str(self.code)}, Nom: {str(self.nom)}, Catégorie: {str(self.categorie)}, Prix: {str(self.prix)}"

    def __repr__(self):
        return f"\nCode produit: {str(self.code)}, \nNom: {str(self.nom)}, \nCatégorie: {str(self.categorie)}, \nPrix: {str(self.prix)}"

    def __eq__(self, autre):
        return self.code == autre.code

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

# --- Tests classe Produit ---
p1 = Produit("P01", "Plat du jour", "plat", 7.20, 20)
p2 = Produit("B01", "Café expresso", "boisson chaude", 1.20, 100)

print(p1)
print(repr(p2))

# Test du tri (__lt__)
assert p2 < p1, "Erreur: Le café devrait être moins cher que le plat"

# Tests de disponibilité
assert p2.est_disponible(150, "08:00") == False, "Erreur: Rupture de stock non détectée"
assert p1.est_disponible(1, "12:00") == True, "Erreur: Le plat devrait être dispo à midi"
assert p1.est_disponible(1, "14:00") == False, "Erreur: Le service des plats finit à 14h00 exclue"
assert p1.est_disponible(1, "11:29") == False, "Erreur: Le service des plats ne commence qu'à 11h30"

print("Tous les tests Produit sont validés !")