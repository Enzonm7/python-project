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

