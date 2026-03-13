class Livre:
    """Représente un livre du fond documentaire."""

    def __init__(self, titre, auteur, numero, nb_exemplaires):
        self._titre = titre
        self._auteur = auteur
        self._numero = numero
        self._nb_exemplaires = nb_exemplaires   # total acheté
        self._nb_empruntes = 0                  # actuellement empruntés

    @property
    def titre(self):
        return self._titre

    @property
    def auteur(self):
        return self._auteur

    @property
    def numero(self):
        return self._numero

    @property
    def nb_exemplaires(self):
        return self._nb_exemplaires

    @property
    def nb_disponibles(self):
        return self._nb_exemplaires - self._nb_empruntes

    @property
    def nb_empruntes(self):
        return self._nb_empruntes

    def est_disponible(self):
        return self.nb_disponibles > 0

    def emprunter(self):
        if not self.est_disponible():
            raise ValueError(f"Aucun exemplaire disponible pour '{self._titre}'.")
        self._nb_empruntes += 1

    def retourner(self):
        if self._nb_empruntes == 0:
            raise ValueError(f"Aucun exemplaire emprunté pour '{self._titre}'.")
        self._nb_empruntes -= 1

    def retirer_exemplaire(self):
        """Retire un exemplaire non emprunté. Retourne False si impossible."""
        if self.nb_disponibles == 0:
            return False
        self._nb_exemplaires -= 1
        return True

    def n_a_plus_d_exemplaire(self):
        return self._nb_exemplaires == 0

    def __str__(self):
        return (f"Livre n°{self._numero} | '{self._titre}' de {self._auteur} | "
                f"Exemplaires : {self._nb_exemplaires} total, "
                f"{self.nb_disponibles} disponible(s)")
