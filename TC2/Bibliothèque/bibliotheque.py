from lecteur import Lecteur
from livre import Livre
from emprunt import Emprunt
from bibliothecaire import Bibliothecaire
from conservateur import Conservateur


class Bibliotheque:
    """Gère le fond documentaire, les lecteurs, les bibliothécaires et les emprunts."""

    def __init__(self, nom, conservateur=None):

        self._nom = nom
        self._conservateur = conservateur
        self._lecteurs = []
        self._livres = []
        self._bibliothecaires = []
        self._emprunts = [] 

    # ------------------------------------------------------------------ #
    #  Propriétés                                                          #
    # ---------------   --------------------------------------------------- #
    @property
    def nom(self):
        return self._nom

    @property
    def conservateur(self):
        return self._conservateur

    @conservateur.setter
    def conservateur(self, c):
        self._conservateur = c

    # ------------------------------------------------------------------ #
    #  Gestion des lecteurs                                                #
    # ------------------------------------------------------------------ #
    def ajout_lecteur(self, nom, prenom, adresse, numero):
        """Ajoute un lecteur. Affiche un message si le numéro existe déjà."""
        if self._trouver_lecteur_par_numero(numero) is not None:
            print(f"Erreur : un lecteur avec le numéro {numero} existe déjà.")
            return
        self._lecteurs.append(Lecteur(nom, prenom, adresse, numero))

    def chercher_lecteur_numero(self, numero):
        """Retourne le Lecteur correspondant au numéro, ou None."""
        return self._trouver_lecteur_par_numero(numero)

    def chercher_lecteur_nom(self, nom, prenom):
        """Retourne le Lecteur correspondant à (nom, prenom), ou None."""
        for l in self._lecteurs:
            if l.nom == nom and l.prenom == prenom:
                return l
        return None

    def retrait_lecteur(self, numero):
        """
        Retire un lecteur s'il n'a plus d'emprunt en cours.
        Retourne True si réussi, False sinon.
        """
        lecteur = self._trouver_lecteur_par_numero(numero)
        if lecteur is None:
            print(f"Retrait lecteur : aucun lecteur avec le numéro {numero}.")
            return False
        if lecteur.a_emprunt_en_cours():
            return False
        self._lecteurs.remove(lecteur)
        return True

    def affiche_lecteurs(self):
        """Affiche tous les lecteurs de la bibliothèque."""
        if not self._lecteurs:
            print("  Aucun lecteur enregistré.")
        for l in self._lecteurs:
            print(l)

    # ------------------------------------------------------------------ #
    #  Gestion des livres                                                  #
    # ------------------------------------------------------------------ #
    def ajout_livre(self, titre, auteur, numero, nb_exemplaires):
        """Ajoute un livre. Affiche un message si le numéro existe déjà."""
        if self._trouver_livre_par_numero(numero) is not None:
            print(f"Erreur : un livre avec le numéro {numero} existe déjà.")
            return
        self._livres.append(Livre(titre, auteur, numero, nb_exemplaires))

    def chercher_livre_numero(self, numero):
        """Retourne le Livre correspondant au numéro, ou None."""
        return self._trouver_livre_par_numero(numero)

    def chercher_livre_titre(self, titre):
        """Retourne le premier Livre dont le titre correspond, ou None."""
        for l in self._livres:
            if l.titre == titre:
                return l
        return None

    def retrait_livre(self, numero):
        """
        Retire un exemplaire disponible du livre (désherbage/vol).
        Si le livre n'a plus d'exemplaire, il est retiré du catalogue.
        Retourne True si réussi, False si aucun exemplaire disponible.
        """
        livre = self._trouver_livre_par_numero(numero)
        if livre is None:
            print(f"Retrait livre : aucun livre avec le numéro {numero}.")
            return False
        if not livre.retirer_exemplaire():
            return False
        if livre.n_a_plus_d_exemplaire():
            self._livres.remove(livre)
        return True

    def affiche_livres(self):
        """Affiche tous les livres de la bibliothèque."""
        if not self._livres:
            print("  Aucun livre enregistré.")
        for l in self._livres:
            print(l)

    # ------------------------------------------------------------------ #
    #  Gestion des emprunts                                                #
    # ------------------------------------------------------------------ #
    def emprunt_livre(self, numero_lecteur, numero_livre):
        """
        Enregistre l'emprunt d'un livre par un lecteur.
        Vérifie la disponibilité et l'absence de double emprunt.
        """
        lecteur = self._trouver_lecteur_par_numero(numero_lecteur)
        if lecteur is None:
            print(f"Emprunt impossible : lecteur n°{numero_lecteur} introuvable.")
            return

        livre = self._trouver_livre_par_numero(numero_livre)
        if livre is None:
            print(f"Emprunt impossible : livre n°{numero_livre} introuvable.")
            return

        if not livre.est_disponible():
            print(f"Emprunt impossible : aucun exemplaire disponible pour "
                  f"'{livre.titre}'.")
            return

        if lecteur.a_deja_emprunte(numero_livre):
            print(f"Emprunt impossible : {lecteur.prenom} {lecteur.nom} a déjà "
                  f"emprunté '{livre.titre}'.")
            return

        emprunt = Emprunt(livre, lecteur)
        livre.emprunter()
        lecteur.ajouter_emprunt(emprunt)
        self._emprunts.append(emprunt)
        print(f"Emprunt enregistré : '{livre.titre}' → "
              f"{lecteur.prenom} {lecteur.nom}")

    def retour_livre(self, numero_lecteur, numero_livre):
        """
        Enregistre le retour d'un livre par un lecteur.
        Affiche un message si l'emprunt est introuvable.
        """
        lecteur = self._trouver_lecteur_par_numero(numero_lecteur)
        if lecteur is None:
            print(f"Retour impossible : lecteur n°{numero_lecteur} introuvable.")
            return

        emprunt_cible = None
        for e in lecteur.emprunts:
            if e.livre.numero == numero_livre:
                emprunt_cible = e
                break

        if emprunt_cible is None:
            print(f"Retour impossible : le lecteur n°{numero_lecteur} n'a pas "
                  f"emprunté le livre n°{numero_livre}.")
            return

        emprunt_cible.enregistrer_retour()
        emprunt_cible.livre.retourner()
        lecteur.retirer_emprunt(emprunt_cible)
        print(f"Retour enregistré : '{emprunt_cible.livre.titre}' ← "
              f"{lecteur.prenom} {lecteur.nom}")

    def affiche_emprunts(self):
        """Affiche tous les emprunts (en cours et terminés)."""
        emprunts_en_cours = [e for e in self._emprunts if e.est_en_cours()]
        if not emprunts_en_cours and not self._emprunts:
            print("  Aucun emprunt enregistré.")
            return
        for e in self._emprunts:
            print(e)

    # ------------------------------------------------------------------ #
    #  Gestion des bibliothécaires                                         #
    # ------------------------------------------------------------------ #
    def ajout_bibliothecaire(self, nom, prenom, numero):
        """Ajoute un bibliothécaire."""
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
        """Affiche tous les bibliothécaires."""
        if self._conservateur:
            print(f"  Conservateur : {self._conservateur}")
        if not self._bibliothecaires:
            print("  Aucun bibliothécaire enregistré.")
        for b in self._bibliothecaires:
            print(f"  {b}")

    # ------------------------------------------------------------------ #
    #  Méthodes internes                                                   #
    # ------------------------------------------------------------------ #
    def _trouver_lecteur_par_numero(self, numero):
        for l in self._lecteurs:
            if l.numero == numero:
                return l
        return None

    def _trouver_livre_par_numero(self, numero):
        for l in self._livres:
            if l.numero == numero:
                return l
        return None

    def _trouver_bibliothecaire(self, numero):
        for b in self._bibliothecaires:
            if b.numero == numero:
                return b
        return None

    def __str__(self):
        return (f"Bibliothèque «{self._nom}» | "
                f"Lecteurs : {len(self._lecteurs)} | "
                f"Livres : {len(self._livres)} | "
                f"Emprunts totaux : {len(self._emprunts)}")
