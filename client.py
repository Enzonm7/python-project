class Client:

    PLAFOND_RECHARGE = 150.0
    DECOUVERT_PERSONNEL = -10.0

    def __init__(self, nom, profil, solde=0.0):
        self.nom = nom
        self.profil = profil
        self.solde = solde
        self.points_fidelite = 0

    def recharger(self, montant):
        if self.profil == "visiteur":
            return False
        if not (5.0 <= montant <= 100.0):
            return False
        if self.solde + montant > Client.PLAFOND_RECHARGE:
            return False
        self.solde += montant
        return True

    def peut_payer(self, montant):
        if self.profil == "visiteur":
            return True
        elif self.profil == "personnel":
            return (self.solde - montant) >= Client.DECOUVERT_PERSONNEL
        elif self.profil in ["étudiant", "alternant"]:
            return (self.solde - montant) > 0
        return False

    def etre_debite(self, montant):
        self.solde -= montant

    def calculer_avantage_fidelite(self, montant_paye):
        if self.profil == "visiteur":
            return 0.0
        remise = 0.0
        if self.points_fidelite >= 30:
            remise = 2.0
            self.points_fidelite -= 30
        self.points_fidelite += int(montant_paye)
        return remise

# --- Tests classe Client ---
c1 = Client("Alice", "étudiant", 12.0)
c2 = Client("Farid", "personnel", 0.0)
c3 = Client("Visiteur", "visiteur")

# Tests recharges
assert c1.recharger(20.0) == True
assert c1.solde == 32.0
assert c1.recharger(130.0) == False
assert c3.recharger(10.0) == False

# Tests paiement et découvert
assert c2.peut_payer(8.0) == True
assert c2.peut_payer(15.0) == False
assert c1.peut_payer(40.0) == False

# Tests fidélité (B1)
c1.points_fidelite = 32
remise = c1.calculer_avantage_fidelite(10.0)
assert remise == 2.0
assert c1.points_fidelite == 12

print("Tous les tests Produit sont validés !")