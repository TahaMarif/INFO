
class Bibliothecaire:
    """Représente un bibliothécaire de la bibliothèque."""

    def __init__(self, nom, prenom, numero):
        self._nom = nom
        self._prenom = prenom
        self._numero = numero

    @property
    def nom(self):
        return self._nom

    @property
    def prenom(self):
        return self._prenom

    @property
    def numero(self):
        return self._numero

    def __str__(self):
        return f"Bibliothécaire n°{self._numero} | {self._prenom} {self._nom}"
