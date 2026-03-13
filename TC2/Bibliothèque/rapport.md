# Rapport de TD — Gestion d'une bibliothèque en Python

---

## En-tête

| Champ | Valeur |
|---|---|
| **Nom** | *Marif Taha* |
| **Numéro de groupe** | *A2-A* |
| **Encadrant** | *Emmanuel DELLANDREA* |
| **Titre du TD** | Programmation orientée objet — Gestion d'une bibliothèque |

---

## Diagramme de classes UML

![Le diagramme ci-dessous présente l'ensemble des classes de l'application, leurs attributs , leurs méthodes (préfixées `+` pour publiques, `-` pour privées) ainsi que les relations entre classes avec leurs cardinalités.](UML_bibliotheque.png)


## Présentation du code — Dernière partie

La dernière partie du TD porte sur la gestion des **bibliothécaires** et du **conservateur**, ainsi que leur intégration dans la classe `Bibliotheque`.

### Classe `Bibliothecaire`

La classe `Bibliothecaire` est simple : elle conserve trois attributs privés (`_nom`, `_prenom`, `_numero`) exposés en lecture seule via des propriétés Python (`@property`).

```python
class Bibliothecaire:
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
```

### Classe `Conservateur` (héritage)

`Conservateur` hérite de `Bibliothecaire` via `Bibliothecaire.__init__()`. Il ne possède pas d'attributs supplémentaires mais représente un rôle distinct (direction de la bibliothèque). Une bibliothèque n'a qu'un seul conservateur (cardinalité 0..1).

```python
from bibliothecaire import Bibliothecaire

class Conservateur(Bibliothecaire):
    def __init__(self, nom, prenom, numero):
        Bibliothecaire.__init__(self, nom, prenom, numero)

    def __str__(self):
        return f"Conservateur n°{self._numero} | {self._prenom} {self._nom}"
```

### Intégration dans `Bibliotheque`

Quatre méthodes publiques gèrent les bibliothécaires, et une méthode privée d'aide interne assure la recherche par numéro :

```python
def ajout_bibliothecaire(self, nom, prenom, numero):
    """Ajoute un bibliothécaire. Vérifie l'unicité du numéro."""
    if self._trouver_bibliothecaire(numero) is not None:
        print(f"Erreur : bibliothécaire n°{numero} existe déjà.")
        return
    self._bibliothecaires.append(Bibliothecaire(nom, prenom, numero))

def retrait_bibliothecaire(self, numero):
    """Retire un bibliothécaire. Retourne True si réussi, False sinon."""
    bib = self._trouver_bibliothecaire(numero)
    if bib is None:
        return False
    self._bibliothecaires.remove(bib)
    return True

def chercher_bibliothecaire(self, numero):
    """Retourne le Bibliothécaire correspondant, ou None."""
    return self._trouver_bibliothecaire(numero)

def affiche_bibliothecaires(self):
    """Affiche le conservateur puis tous les bibliothécaires."""
    if self._conservateur:
        print(f"  Conservateur : {self._conservateur}")
    if not self._bibliothecaires:
        print("  Aucun bibliothécaire enregistré.")
    for b in self._bibliothecaires:
        print(f"  {b}")

def _trouver_bibliothecaire(self, numero):
    """Méthode privée : parcourt la liste et retourne l'instance ou None."""
    for b in self._bibliothecaires:
        if b.numero == numero:
            return b
    return None
```

### Points de conception

-L'attribut `_conservateur` est initialisé à `None` dans le constructeur de `Bibliotheque` et peut être assigné via un setter `@conservateur.setter`. Cela permet de créer une bibliothèque sans conservateur désigné, ou de le changer en cours de vie de l'objet.

-Conformément à l'interface attendue par le programme principal, les méthodes `retrait_bibliothecaire`, `retrait_lecteur` et `retrait_livre` retournent un booléen (`True`/`False`) plutôt que de lever une exception.

-Le pattern `_trouver_*(numero)` est systématiquement utilisé en interne dans `Bibliotheque` pour toutes les collections (lecteurs, livres, bibliothécaires).
