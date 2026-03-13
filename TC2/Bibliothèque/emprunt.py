from datetime import date

class Emprunt:
    """Représente l'emprunt d'un livre par un lecteur."""

    def __init__(self, livre, lecteur, date_emprunt=None):
        self._livre = livre
        self._lecteur = lecteur
        self._date_emprunt = date_emprunt if date_emprunt else date.today()
        self._date_retour = None

    @property
    def livre(self):
        return self._livre

    @property
    def lecteur(self):
        return self._lecteur

    @property
    def date_emprunt(self):
        return self._date_emprunt

    @property
    def date_retour(self):
        return self._date_retour

    def est_en_cours(self):
        return self._date_retour is None

    def enregistrer_retour(self, date_retour=None):
        self._date_retour = date_retour if date_retour else date.today()

    def __str__(self):
        statut = 'en cours' if self.est_en_cours() else f'rendu le {self._date_retour}'
        return (f"Emprunt | Livre n°{self._livre.numero} '{self._livre.titre}' | "
                f"Lecteur : {self._lecteur.prenom} {self._lecteur.nom} "
                f"(n°{self._lecteur.numero}) | "
                f"Emprunté le : {self._date_emprunt} | Statut : {statut}")
