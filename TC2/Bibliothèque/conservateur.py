from bibliothecaire import Bibliothecaire

class Conservateur(Bibliothecaire):
    """Dirige la bibliothèque. Hérite de Bibliothécaire."""

    def __init__(self, nom, prenom, numero):
        super().__init__(nom, prenom, numero)

    def __str__(self):
        return f"Conservateur n°{self._numero} | {self._prenom} {self._nom}"
