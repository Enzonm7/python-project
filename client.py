class Client:

    PLAFOND_RECHARGE = 150.0
    DECOUVERT_PERSONNEL = -10.0

    def __init__(self, nom, profil, solde=0.0):
        self.nom = nom
        self.profil = profil
        self.solde = solde
        self.points_fidelite = 0