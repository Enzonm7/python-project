class Client:

    PLAFOND_RECHARGE = 150.0
    DECOUVERT_PERSONNEL = -10.0
    RECHARGE_MIN = 5.0
    RECHARGE_MAX = 100.0
    SEUIL_FIDELITE = 30
    MONTANT_BON_FIDELITE = 2.0

    def __init__(self, nom, profil, solde=0.0):
        self.nom = nom
        self.profil = profil
        self.solde = solde
        self.points_fidelite = 0

    def __repr__(self):
        return f"Client('{self.nom}', '{self.profil}', {self.solde})"

    def a_un_badge(self):
        return self.profil != "visiteur"

    def recharger(self, montant):
        if not self.a_un_badge():
            return False
        if not (Client.RECHARGE_MIN <= montant <= Client.RECHARGE_MAX):
            return False
        if self.solde + montant > Client.PLAFOND_RECHARGE:
            return False
        self.solde += montant
        return True

    def peut_payer(self, montant):
        if not self.a_un_badge():
            return True
        if self.profil == "personnel":
            return (self.solde - montant) >= Client.DECOUVERT_PERSONNEL
        if self.profil in ["étudiant", "alternant"]:
            return (self.solde - montant) >= 0
        return False

    def etre_debite(self, montant):
        if self.a_un_badge():
            self.solde -= montant

    def a_droit_au_bon(self):
        return self.a_un_badge() and self.points_fidelite >= Client.SEUIL_FIDELITE

    def actualiser_fidelite(self, montant_paye):
        if not self.a_un_badge():
            return
        if self.a_droit_au_bon():
            self.points_fidelite -= Client.SEUIL_FIDELITE
        self.points_fidelite += int(montant_paye)