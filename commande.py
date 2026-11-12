class Commande:

    COMPTEUR_NUMERO = 1

    def __init__(self, client, heure):
        self.numero = Commande.COMPTEUR_NUMERO
        Commande.COMPTEUR_NUMERO += 1
        self.client = client
        self.heure = heure
        self.lignes = {}

    def ajouter_lignes(self, produit, quantite):
        if produit in self.lignes:
            self.lignes[produit] += quantite
        else:
            self.lignes[produit] = quantite

    def __len__(self):
        return sum(self.lignes.values())

    def __contains__(self, produit):
        return produit in self.lignes

    def __iter__(self):
        return iter(self.lignes.items())