class Cafeteria:

    def __init__(self, nom):
        self.nom = nom
        self.catalogue = {}
        self.clients = {}
        self.commandes = []
        self.chiffre_affaires = 0.0