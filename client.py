class Client:
    """Représente un client de la cafétéria (titulaire d'un badge ou visiteur au comptant) et gère son solde et sa fidélité."""

    PLAFOND_RECHARGE = 150.0
    DECOUVERT_PERSONNEL = -10.0
    RECHARGE_MIN = 5.0
    RECHARGE_MAX = 100.0
    SEUIL_FIDELITE = 30
    MONTANT_BON_FIDELITE = 2.0

    def __init__(self, nom, profil, solde=0.0):
        """Initialise un client avec son nom, son profil ('étudiant', 'alternant', 'personnel', 'visiteur') et son solde."""
        self.nom = nom
        self.profil = profil
        self.solde = solde
        self.points_fidelite = 0
        self.commandes = []

    def __repr__(self):
        """Renvoie la représentation technique du client."""
        return f"Client('{self.nom}', '{self.profil}', {self.solde})"

    def a_un_badge(self):
        """Indique si le client possède un badge (tout le monde sauf les visiteurs)."""
        return self.profil != "visiteur"

    def recharger(self, montant):
        """Crédite le badge si le client en a un, que le montant est entre 5 € et 100 €, et sans dépasser le plafond de 150 €."""
        if not self.a_un_badge():
            return False
        if not (Client.RECHARGE_MIN <= montant <= Client.RECHARGE_MAX):
            return False
        if self.solde + montant > Client.PLAFOND_RECHARGE:
            return False
        self.solde += montant
        return True

    def peut_payer(self, montant):
        """Vérifie si le client peut régler le montant (comptant pour un visiteur, découvert de -10 € autorisé pour le personnel)."""
        if not self.a_un_badge():
            return True
        if self.profil == "personnel":
            return (self.solde - montant) >= Client.DECOUVERT_PERSONNEL
        if self.profil in ["étudiant", "alternant"]:
            return (self.solde - montant) >= 0
        return False

    def etre_debite(self, montant):
        """Retire le montant du solde uniquement si le client possède un badge (un visiteur paie comptant)."""
        if self.a_un_badge():
            self.solde -= montant

    def a_droit_au_bon(self):
        """Vérifie sans modifier les points si le client a un badge et atteint le seuil de 30 points de fidélité."""
        return self.a_un_badge() and self.points_fidelite >= Client.SEUIL_FIDELITE

    def actualiser_fidelite(self, montant_paye):
        """Met à jour les points après paiement : retire 30 points si le bon a été utilisé, puis ajoute 1 point par euro entier payé."""
        if not self.a_un_badge():
            return
        if self.a_droit_au_bon():
            self.points_fidelite -= Client.SEUIL_FIDELITE
        self.points_fidelite += int(montant_paye)

    def rejouer_fidelite(self, commandes):
        self.points_fidelite = 0
        if not self.a_un_badge():
            return
        for commande in commandes:
            if commande.statut != "annulée" and commande.montant_paye is not None:
                self.actualiser_fidelite(commande.montant_paye)