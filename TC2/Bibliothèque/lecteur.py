class Lecteur:
    """Représente un lecteur inscrit dans la bibliothèque."""

    def __init__(self, nom, prenom, adresse, numero):
        self._nom = nom
        self._prenom = prenom
        self._adresse = adresse
        self._numero = numero
        self._emprunts = []  

    @property
    def nom(self):
        return self._nom

    @property
    def prenom(self):
        return self._prenom

    @property
    def adresse(self):
        return self._adresse

    @property
    def numero(self):
        return self._numero

    @property
    def emprunts(self):
        return self._emprunts

    def ajouter_emprunt(self, emprunt):
        self._emprunts.append(emprunt)

    def retirer_emprunt(self, emprunt):
        if emprunt in self._emprunts:
            self._emprunts.remove(emprunt)

    def a_emprunt_en_cours(self):
        return len(self._emprunts) > 0

    def a_deja_emprunte(self, numero_livre):
        return any(e.livre.numero == numero_livre for e in self._emprunts)

    def __str__(self):
        nb = len(self._emprunts)
        livres = ', '.join(str(e.livre.numero) for e in self._emprunts) if nb else 'aucun'
        return (f"Lecteur n°{self._numero} | {self._prenom} {self._nom} | "
                f"{self._adresse} | Emprunts en cours : {nb} ({livres})")
